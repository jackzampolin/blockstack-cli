import click
import requests
import blockstack

class Config(object):
    
    def __init__(self):
        self.host = 'localhost:6270'
        self.directory = '~/.blockstack'

pass_config = click.make_pass_decorator(Config, ensure=True)

###########################
# GROUP: blockstack-cli
# blockstack-cli
###########################
@click.group()
@click.option('--host', default='localhost:6270', help='blockstack api node to connect to ')
@click.option('--directory', default='~/.blockstack', help='directory for blockstack configuration and data files')
@pass_config
def cli(config, host, directory):
    """A command line interface for the blockstack network and local installations"""
    config.host = host
    config.directory = directory

###########################
# GROUP: NODE
# blockstack-cli node
###########################
@cli.group()
@pass_config
def node(config):
    """commands for conifguring and reaching blockstack api nodes"""
    pass
        
# blockstack-cli node ping
# https://blockstack.github.io/blockstack-core/#core-node-administration-ping-the-node
@node.command()
@pass_config
def ping(config):
    """check availibiltiy for connected node"""
    click.echo(blockstack.blockstack_client.ping())
    
# GROUP: NODE CONFIG
# blockstack-cli node config
@node.group()
@pass_config
def config(config):
    """configuration commands for connected node"""
    pass

# blockstack-cli node config get
# https://blockstack.github.io/blockstack-core/#core-node-administration-get-the-node-s-config
@config.command()
@pass_config
def get(config):
    """retrieve configuration for connected node"""
    click.echo(blockstack.blockstack_client.read_config_file())

# blockstack-cli node config set
# https://blockstack.github.io/blockstack-core/#core-node-administration-set-config-field
@config.command()
@click.argument('SECTION')
@click.argument('KEY')
@click.argument('VALUE')
@pass_config
def set(config, section, key, value):
    """reset configuration KEY in SECTION to VALUE for configured node"""
    click.echo('setting key {} in section {} on {} to {}...'.format(key,section,config.host,value))

# blockstack-cli node config delete
# https://blockstack.github.io/blockstack-core/#core-node-administration-delete-a-config-field
@config.command()
@click.argument('SECTION')
@click.argument('KEY')
@pass_config
def delete(config, section, key):
    """remove configuration KEY in SECTION for configured node"""
    click.echo('deleting key {} in section {} on {}...'.format(key,section,config.host))

# blockstack-cli node config delete_section
# https://blockstack.github.io/blockstack-core/#core-node-administration-delete-a-config-section
@config.command()
@click.argument('SECTION')
@pass_config
def delete_section(config, section):
    """remove configuration SECTION for configured node"""
    click.echo('deleting section {} on {}...'.format(section,config.host))

# blockstack-cli node registrar
# https://blockstack.github.io/blockstack-core/#core-node-administration-get-registrar-state
@node.command()
@pass_config
def registrar(config):
    """check registrar state"""
    click.echo('checking registrar state...')

# blockstack-cli node methods
# This is for development and lets me print methods from different modules
@node.command()
@pass_config
def methods(config):
    """print out blockstack_client methods"""
    click.echo(dir(blockstack.blockstack_client))
    
###########################
# GROUP: WALLET
# blockstack-cli wallet
###########################
@cli.group()
@pass_config
def wallet(config):
    """commands to perform operations on your blockstack wallet"""
    pass

# blockstack-cli wallet payment_address
# https://blockstack.github.io/blockstack-core/#core-wallet-management-get-wallet-payment-address
@wallet.command()
@pass_config
def payment_address(config):
    """retrieve the payment_address for your blockstack wallet"""
    click.echo("blockstack wallet payment_address")

# blockstack-cli wallet owner_address
# https://blockstack.github.io/blockstack-core/#core-wallet-management-get-wallet-owner-address
@wallet.command()
@pass_config
def owner_address(config):
    """retrieve the owner_address for your blockstack wallet"""
    click.echo("blockstack wallet owner_address")

# blockstack-cli wallet pub_key
# https://blockstack.github.io/blockstack-core/#core-wallet-management-get-wallet-data-public-key
@wallet.command()
@pass_config
def pub_key(config):
    """retrieve the pub_key for your blockstack wallet"""
    click.echo("blockstack wallet pub_key")

# blockstack-cli wallet set_key
# https://blockstack.github.io/blockstack-core/#core-wallet-management-set-a-specific-wallet-key
@wallet.command()
@click.argument('KEY')
@pass_config
def set_key(config, key):
    """set a specific key to use"""
    click.echo("using wallet with key {}".format(key))

# blockstack-cli wallet balance
# https://blockstack.github.io/blockstack-core/#core-wallet-management-get-payment-wallet-balance
@wallet.command()
@click.option('--confirmations', default=6, help='number of confirmations to include transactions in wallet balance')
@pass_config
def balance(config, confirmations):
    """retrieve wallet balance"""
    click.echo("blockstack wallet balance")

# blockstack-cli wallet send
# https://blockstack.github.io/blockstack-core/#core-wallet-management-withdraw-payment-wallet-funds
@wallet.command()
@click.option('--confirmations', default=6, help='number of confirmations to include transactions in wallet balance')
@click.option('--tx_only', is_flag=True, help='a flag?')
@click.argument('AMOUNT')
@click.argument('ADDRESS')
@pass_config
def send(config,amount,address,confirmations,tx_only):
    """send AMOUNT to ADDRESS..."""
    click.echo("sending {} to {} after {} confirmations...".format(amount, address, confirmations))

###########################
# GROUP: NAME
# blockstack-cli name
###########################
@cli.group()
@pass_config
def name(config):
    """commands for name operations"""
    pass

# blockstack-cli name register
# https://blockstack.github.io/blockstack-core/#managing-names-register-a-name
@name.command()
@click.argument('NAME')
@pass_config
def register(config, name):
    """register a NAME"""
    click.echo('register for {}'.format(name))

# blockstack-cli name revoke
# https://blockstack.github.io/blockstack-core/#managing-names-revoke-name
@name.command()
@click.argument('NAME')
@pass_config    
def revoke(config, name):
    """revoke NAME"""
    click.echo('revoke for {}'.format(name))

# blockstack-cli name transfer
# https://blockstack.github.io/blockstack-core/#managing-names-transfer-name
@name.command()
@click.argument('NAME')
@click.argument('OWNER')
@pass_config    
def transfer(config, name, owner):
    """transfer NAME to OWNER"""
    click.echo('transfer {} to {}'.format(name, owner))

# blockstack-cli name set_zonefile
# https://blockstack.github.io/blockstack-core/#managing-names-set-zone-file
@name.command()
@click.argument('NAME')
@click.argument('JSON', type=click.File('rb'))
@pass_config    
def set_zonefile(config, name, json):
    """set zonefile for NAME"""
    click.echo('set_zonefile for {} from zonefile {}'.format(name, json))

# blockstack-cli name get_zonefile
# https://blockstack.github.io/blockstack-core/#managing-names-fetch-zone-file
@name.command()
@click.argument('NAME')
@pass_config    
def get_zonefile(config, name):
    """get zonefile for NAME"""
    click.echo('get_zonefile for {}'.format(name))

# blockstack-cli name get_page
# https://blockstack.github.io/blockstack-core/#name-querying-get-all-names
@name.command()
@click.argument('PAGE')
@pass_config
def get_page(config,page):
    """get a page from the list all blockstack names"""
    click.echo("{}".format(name)) 

# blockstack-cli name get
# https://blockstack.github.io/blockstack-core/#name-querying-get-name-info
@name.command()
@click.argument('NAME')
@pass_config
def get(config,name):
    """get details for a name"""
    click.echo("getting {} details".format(name)) 

# blockstack-cli name history
# https://blockstack.github.io/blockstack-core/#name-querying-name-history
@name.command()
@click.argument('NAME')
@pass_config
def history(config,name):
    """get the transfer history for a name"""
    click.echo("getting history for {}".format(name)) 

# blockstack-cli name zonefile_history
# https://blockstack.github.io/blockstack-core/#name-querying-get-historical-zone-file
@name.command()
@click.argument('NAME')
@click.argument('ZONEFILEHASH')
@pass_config
def zonefile_history(config,name,zonefilehash):
    """zonefile_history name thing"""
    click.echo("getting zonefile history for {} from zonefilehash {}".format(name,zonefilehash)) 

# blockstack-cli name address
# https://blockstack.github.io/blockstack-core/#name-querying-get-names-owned-by-address
@name.command()
@click.argument('ADDRESS')
@click.option('--blockchain', default='bitcoin', help='blockchain to which address belongs. Currently only bitcoin is supported')
@pass_config
def address(config,address,blockchain):
    """address name thing"""
    click.echo("Finding names associated with address {} on the {} blockchain".format(address,blockchain)) 

###########################
# GROUP: PRICE
# blockstack-cli price
###########################
@cli.group()
@pass_config
def price(config):
    """query the price of names or namespaces"""
    pass

# blockstack-cli price namespace 
# https://blockstack.github.io/blockstack-core/#price-checks-get-namespace-price
@price.command()
@click.argument('NAMESPACE')
@pass_config
def namespace(config,namespace):
    """get the price for a namespace"""
    click.echo("Fetching price for namespace {}...".format(namespace))

# blockstack-cli price name 
# https://blockstack.github.io/blockstack-core/#price-checks-get-name-price
@price.command()
@click.argument('name')
@pass_config
def name(config,name):
    """get the price for a name"""
    click.echo("Fetching price for name {}...".format(name))

###########################
# GROUP: BLOCKCHAIN
# blockstack-cli blockchain
###########################
@cli.group()
@pass_config
def blockchain(config):
    """perform blockchain operations with your connected node"""
    pass

# blockstack-cli blockchain get_consensus
# https://blockstack.github.io/blockstack-core/#blockchain-operations-get-consensus-hash
@blockchain.command()
@click.option('--blockchain', default='bitcoin', help='blockchain to which address belongs. Currently only bitcoin is supported')
@pass_config
def get_consensus(config,blockchain):
    """get_consensus hash from the connected blockchain node"""
    click.echo('fetching consensus hash from {} node...'.format(blockchain))

# blockstack-cli blockchain get_pending
# https://blockstack.github.io/blockstack-core/#blockchain-operations-get-pending-transactions    
@blockchain.command()
@click.option('--blockchain', default='bitcoin', help='blockchain to which address belongs. Currently only bitcoin is supported')
@pass_config
def get_pending(config,blockchain):
    """get_pending transactions from connected blockchain node"""
    click.echo('getting pending {} from connected node...'.format(blockchain))

# blockstack-cli blockchain get_utxo
# https://blockstack.github.io/blockstack-core/#blockchain-operations-get-unspent-outputs
@blockchain.command()
@click.option('--blockchain', default='bitcoin', help='blockchain to which address belongs. Currently only bitcoin is supported')
@click.argument('ADDRESS')
@pass_config
def get_utxo(config,blockchain,address):
    """get unspent transaction outputs from an ADDRESS"""
    click.echo("getting utxo from {} address {}...".format(blockchain,address))

# blockstack-cli blockchain send_transaction
# https://blockstack.github.io/blockstack-core/#blockchain-operations-broadcast-transaction
@blockchain.command()
@click.option('--blockchain', default='bitcoin', help='blockchain to which address belongs. Currently only bitcoin is supported')
@click.argument('JSON', type=click.File('rb'))
@pass_config
def send_transaction(config,blockchain,json):
    """send a transaction to the underlying blockchain"""
    click.echo('Sending transaction to the {} blockchain from file {}...'.format(blockchain,json))
    

###########################
# GROUP: GAIA
# blockstack-cli gaia
###########################
@cli.group()
@pass_config
def gaia(config):
    """these are gaia commands"""
    click.echo('Hello gaia')

# blockstack-cli gaia store
@gaia.group()
@pass_config
def store(config):
    """store"""
    pass
    
# blockstack-cli gaia store create
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-create-store-for-this-session
@store.command()
@pass_config
def create(config):
    """make a new session store for gaia storage"""
    click.echo("creating new store...")
    
# blockstack-cli gaia store get
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-get-store-metadata
@store.command()
@click.argument("STORE")
@pass_config
def get(config,store):
    """retrieve STORE details"""
    click.echo("getting info about store {}...".format(store))
    
# blockstack-cli gaia store delete
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-delete-store-
@store.command()
@click.argument("STORE")
@pass_config
def delete(config,store):
    """remove a STORE"""
    click.echo("getting info about store {}...".format(store))

# blockstack-cli gaia inode 
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-get-inode-info
@gaia.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def inode(config,store,path):
    """get info about inode at PATH from STORE"""
    click.echo("getting info about inode in store {} at path {}...".format(store,path))
    
# blockstack-cli gaia directory
@gaia.group()
@pass_config
def directory(config):
    """crud for gaia directories"""
    pass
    
# blockstack-cli gaia directory files
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-get-directory-files
@directory.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def files(config,store,path):
    """get files in directory at PATH from STORE"""
    click.echo("files in path {} from store {}...".format(path,store))

# blockstack-cli gaia directory create
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-create-directory
@directory.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def create(config,store,path):
    """create directory at PATH from STORE"""
    click.echo("create in path {} from store {}...".format(path,store))

# blockstack-cli gaia directory delete
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-delete-directory
@directory.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def delete(config,store,path):
    """delete directory at PATH from STORE"""
    click.echo("delete in path {} from store {}...".format(path,store))

# blockstack-cli gaia file
@gaia.group()
@pass_config
def file(config):
    """crud for gaia files"""
    pass
    
# blockstack-cli gaia file get
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-get-file-data
@file.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def get(config,store,path):
    """get file at given PATH from STORE"""
    click.echo("get file at path {} from store {}...".format(path,store))
    
# blockstack-cli gaia file create
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-create-file
@file.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def create(config,store,path):
    """create file at given PATH from STORE"""
    click.echo("create file at path {} from store {}...".format(path,store))
    
# blockstack-cli gaia file update
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-update-file
@file.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def update(config,store,path):
    """update file at given PATH from STORE"""
    click.echo("update file at path {} from store {}...".format(path,store))
    
# blockstack-cli gaia file delete
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-delete-file
@file.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def delete(config,store,path):
    """delete file at given PATH from STORE"""
    click.echo("delete file at path {} from store {}...".format(path,store))


###########################
# GROUP: NAMESPACE
# blockstack-cli namespace
###########################
@cli.group()
@pass_config
def namespace(config):
    """these are namespace commands"""
    click.echo('Hello namespace')
    
# blockstack-cli namespace all
# https://blockstack.github.io/blockstack-core/#namespace-operations-get-all-namespaces
@namespace.command()
@pass_config
def all(config):
    """get all namespaces"""
    click.echo("getting all namespaces...")

# blockstack-cli namespace names
# https://blockstack.github.io/blockstack-core/#namespace-operations-get-namespace-names
@namespace.command()
@click.argument("PAGE")
@pass_config
def names(config):
    """get a PAGE of names from a namespace"""
    click.echo("get all namespaces")