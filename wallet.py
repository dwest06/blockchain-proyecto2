import names
import random
import blocksmith

class Wallet(object):
    """
    Almacenamiento para private key de usuarios
    """

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    @classmethod
    def generate_random_person(cls):
        name = names.get_first_name()
        email = f"{name}-{random.randint(0,999)}@testmail.com"
        return cls(name, email)

    def generate_keys(self):
        # https://github.com/Destiner/blocksmith
        input_data = f"{self.name} {self.email}"

        # Generate privkey
        kg = blocksmith.KeyGenerator()
        kg.seed_input(input_data)
        self.privkey = kg.generate_key()

        # Generate pubkey from privkey
        self.pubkey = blocksmith.EthereumWallet._EthereumWallet__private_to_public(self.privkey).decode()
        
        # Generate address from pubkey
        self.address = blocksmith.EthereumWallet._EthereumWallet__public_to_address(self.pubkey)

        # Generate address from privkey
        # address = blocksmith.EthereumWallet.generate_address(privkey)

        # Generate checksum address
        self.checksum_address = blocksmith.EthereumWallet.checksum_address(self.address)