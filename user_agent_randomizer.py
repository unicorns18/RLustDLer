import os
from prng.chacha20_prng import ChaCha20PRNG
from useragents.useragents import ChromeUAs, FirefoxUAs, SafariUAs

class UserAgentRandomizer:
    def __init__(self):
        self.user_agents = [ChromeUAs, FirefoxUAs, SafariUAs]
        self.key = os.urandom(32)
        self.nonce = os.urandom(12)
        self.rng = ChaCha20PRNG(self.key, self.nonce)

    def _choice(self, seq):
        idx = self.rng.randint(0, len(seq)-1)
        return seq[idx]

    def get_random_ua(self):
        browser = self._choice(self.user_agents)
        ua = self._choice(list(browser))
        return ua.value  # Return the value of the enum member

    def get_random_chrome_ua(self):
        return self._choice(list(ChromeUAs)).value

    def get_random_firefox_ua(self):
        return self._choice(list(FirefoxUAs)).value

    def get_random_safari_ua(self):
        return self._choice(list(SafariUAs)).value

if __name__ == '__main__':
    uar = UserAgentRandomizer()
    print(uar.get_random_ua())