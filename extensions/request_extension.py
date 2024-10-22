import re
import uuid
from interactions import Button, ButtonStyle, Embed, EmbedField, Extension, Color, OptionType
import interactions

from backblazeapi import BackblazeUploader
from crawler import VideoCrawler
from rlust_downloader import RLustDownloader

class RequestExtension(Extension):
    def __init__(self, bot: interactions.Client):
        self.bot = bot
        self.rlust_downloader = RLustDownloader()

        # backblaze
        self.key_id = "0052fc0012fb1e30000000001"
        self.application_key = "K005XND/ukcRD5RYlhjHuSMARFqE9Ss"
        self.bucket_name = "UnicornsPrivateVideos"
        self.endpointurl = "https://s3.us-east-005.backblazeb2.com"
        self.backblaze_uploader = BackblazeUploader(
            key_id=self.key_id,
            application_key=self.application_key,
            bucket_name=self.bucket_name
        )
    
    @interactions.slash_command(
        name="request",
        description="give it a url"
    )
    @interactions.slash_option(
        name="url",
        description="URL of the video to request",
        required=True,
        opt_type=OptionType.STRING
    )
    async def request(self, ctx, url):
        await ctx.defer(ephemeral=True)

        if not self.is_valid_url(url):
            await ctx.send("Invalid URL", ephemeral=True)
            return

        with VideoCrawler() as crawler:
            video_info = crawler.get_video_info(url)
            if not video_info:
                await ctx.send("Failed to get video info", ephemeral=True)
                return
            video_url = video_info.video_url
            video_type = video_info.video_type
            print(f"Video URL: {video_url}, Video Type: {video_type}")
            await ctx.send("downloading video now...", ephemeral=True)
            user_id = ctx.author.id
            random_id = str(uuid.uuid4())[:8]
            file_extension = self.get_file_extension(video_type)
            print(f"File Extension: {file_extension}")
            filename = f"{user_id}_{random_id}.{file_extension}"
            self.rlust_downloader.download(video_url, output_filename=filename)
            public_url = self.backblaze_uploader.upload_file(filename)
            if not public_url:
                await ctx.send("Failed to upload video", ephemeral=True)
                return
            self.rlust_downloader.delete_file(filename)
            user = await self.bot.fetch_user(user_id)
            await user.send(public_url)

    def get_file_extension(self, video_type: str) -> str:
        if 'mp4' in video_type:
            return '.mp4'
        elif 'quicktime' in video_type:
            return '.mov'
        else:
            print(f"unrecognized filetype: {video_type}")
            return '.mp4'
        
    def is_valid_url(self, url: str) -> bool:
        regex = re.compile(r"https?://[\w.-]+")
        return bool(regex.match(url))