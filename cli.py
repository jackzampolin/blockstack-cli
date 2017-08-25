import click
import requests
import json
import toml
import yaml
import os

class Config(object):
    
    def __init__(self):
        self.host = 'localhost:6270'
        self.method = 'http://'
        self.password = 'foobarbaz'
        self.debug = False
        self.fmt = 'json'

pass_config = click.make_pass_decorator(Config, ensure=True)

# HELPER METHODS
def create_url(config, path):
    return "{}{}{}".format(config.method,config.host,path)

def make_headers(config):
    return {'Authorization': 'bearer {}'.format(config.password), 'Origin': 'http://localhost:3000', 'Content-Type': 'application/json'}

def make_debug_headers(config):
    return {'Authorization': 'bearer PASSWORD_OMITTED', 'Origin': 'http://localhost:3000', 'Content-Type': 'application/json'}

def json_out(r):
    return json.dumps(r,sort_keys=True, indent=4, separators=(',', ': '))

def output(config, url, r):
    if config.debug:
        click.echo("Request URL: {} {}".format(r.request.method, url))
        click.echo("Request Headers:\n{}".format(json_out(make_debug_headers(config))))
        if r.request.body:
            click.echo("Request Payload:\n{}".format(json_out(json.loads(r.request.body))))
        click.echo("Response Code: {}".format(r.status_code))
        click.echo("Response Body ({}):".format(config.fmt))
    
    if config.fmt == "json":
        if r.text:
            click.echo(json_out(r.json()))
    elif config.fmt == "yaml":
        if r.text:
            click.echo(yaml.safe_dump(r.json(), default_flow_style=False))
    elif config.fmt == "toml":
        if r.text:
            click.echo(toml.dumps(r.json()))
    else:
        click.echo("not a supported output format")

# Default Configuration
default_config = {
  'subdomain-resolution': {
    'subdomains_db': '{}.blockstack/subdomains.db'.format(os.environ["HOME"]),
  },
  'blockstack-client': {
    'api_endpoint_host': 'localhost',
    'blockchain_writer': 'blockstack_utxo',
    'api_endpoint_port': '6270',
    'api_password': '{}'.format(os.urandom(32).encode('base-64')[:-2]),
    'poll_interval': '300',
    'server': 'node.blockstack.org',
    'email': '',
    'metadata': 'metadata',
    'storage_drivers_required_write': 'disk,dropbox',
    'queue_path': '{}.blockstack/queues.db'.format(os.environ["HOME"]),
    'storage_drivers': 'disk,dropbox,s3,blockstack_resolver,blockstack_server,http,dht',
    'blockchain_reader': 'blockstack_utxo',
    'client_version': '0.14.4.2',
    'api_endpoint_bind': 'localhost',
    'port': 6264,
    'anonymous_statistics': True,
  },
  'bitcoind': {
    'passwd': 'blockstacksystem',
    'regtest': 'False',
    'spv_path': '{}.virtualchain-spv-headers.dat'.format(os.environ["HOME"]),
    'server': 'bitcoin.blockstack.com',
    'p2p_port': '8333',
    'user': 'blockstack',
    'timeout': '300',
    'port': '8332',
  },
  'blockstack': {
    'server': 'node.blockstack.org',
  },
  'blockchain-writer': {
    'url': 'https://utxo.blockstack.org',
    'utxo_provider': 'blockstack_utxo',
  },
  'blockchain-reader': {
    'url': 'https://utxo.blockstack.org',
    'utxo_provider': 'blockstack_utxo',
  },
}

###########################
# GROUP: blockstack-cli
# blockstack-cli
###########################
@click.group()
@click.option('-host', default='localhost:6270', help='blockstack api node to connect to ', envvar="BLOCKSTACK_CLI_HOST")
@click.option('-ssl', is_flag=True)
@click.option('-debug', is_flag=True)
@click.option('-password', default='foobarbaz', help='api password for instance to connect', envvar="BLOCKSTACK_CLI_PASSWORD")
@click.option('-fmt', default='json', help='format to output responses {json|toml|yaml}')
@pass_config
def cli(config, host, password, ssl, debug, fmt):
    """A command line interface for the blockstack network and local installations"""
    config.host = host
    config.debug = debug
    config.password = password
    config.fmt = fmt
    if ssl:
        config.method = "https://"
    else:
        config.method = "http://"

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
    url = create_url(config,"/v1/node/ping")
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli node registrar
# https://blockstack.github.io/blockstack-core/#core-node-administration-get-registrar-state
@node.command()
@pass_config
def registrar(config):
    """check registrar state"""
    path = "/v1/node/registrar/state"
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)
    
###########################
# GROUP: CONFIG
# blockstack-cli config
###########################
@cli.group()
@pass_config
def config(config):
    """configuration commands for connected node"""
    pass

# blockstack-cli config get
# https://blockstack.github.io/blockstack-core/#core-node-administration-get-the-node-s-config
@config.command()
@pass_config
def get(config):
    """print TOML config for current node"""
    path = "/v1/node/config"
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli config default
# https://blockstack.github.io/blockstack-core/#core-node-administration-get-the-node-s-config
@config.command()
@pass_config
def default(config):
    """print default TOML config to STDOUT"""
    click.echo(toml.dumps(default_config))

# blockstack-cli config set
# https://blockstack.github.io/blockstack-core/#core-node-administration-set-config-field
@config.command()
@click.argument('SECTION')
@click.argument('KEY')
@click.argument('VALUE')
@pass_config
def set(config, section, key, value):
    """reset configuration KEY in SECTION to VALUE for configured node"""
    path = "/v1/node/config/{}?{}={}".format(section,key,value)
    url = create_url(config,path)
    r = requests.post(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli config delete
# https://blockstack.github.io/blockstack-core/#core-node-administration-delete-a-config-field
@config.command()
@click.argument('SECTION')
@click.argument('KEY')
@pass_config
def delete(config, section, key):
    """remove configuration KEY in SECTION for configured node"""
    path = "/v1/node/config/{}/{}".format(section,key)
    url = create_url(config,path)
    r = requests.delete(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli config delete_section
# https://blockstack.github.io/blockstack-core/#core-node-administration-delete-a-config-section
@config.command()
@click.argument('SECTION')
@pass_config
def delete_section(config, section):
    """remove configuration SECTION for configured node"""
    path = "/v1/node/config/{}".format(section)
    url = create_url(config,path)
    r = requests.delete(url, headers=make_headers(config))
    output(config, url, r)
    
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
    path = "/v1/wallet/payment_address"
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli wallet owner_address
# https://blockstack.github.io/blockstack-core/#core-wallet-management-get-wallet-owner-address
@wallet.command()
@pass_config
def owner_address(config):
    """retrieve the owner_address for your blockstack wallet"""
    path = "/v1/wallet/owner_address"
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)
    
# blockstack-cli wallet pub_key
# https://blockstack.github.io/blockstack-core/#core-wallet-management-get-wallet-data-public-key
@wallet.command()
@pass_config
def pub_key(config):
    """retrieve the pub_key for your blockstack wallet"""
    path = "/v1/wallet/data_pubkey"
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)
    
# NOT IMPLEMENTED
# blockstack-cli wallet set_key
# https://blockstack.github.io/blockstack-core/#core-wallet-management-set-a-specific-wallet-key
@wallet.command()
@click.argument('KEY')
@pass_config
def set_key(config, key):
    """set a specific key to use"""
    click.echo("NOT IMPLEMENTED")
    click.echo("arg passed:")
    click.echo("  KEY -> {}".format(key))


# blockstack-cli wallet balance
# https://blockstack.github.io/blockstack-core/#core-wallet-management-get-payment-wallet-balance
@wallet.command()
@click.option('--confirmations', default=6, help='number of confirmations to include transactions in wallet balance')
@pass_config
def balance(config, confirmations):
    """retrieve wallet balance"""
    path = "/v1/wallet/balance/{}".format(confirmations)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# NOT IMPLEMENTED
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
    click.echo("NOT IMPLEMENTED, TEST ON REGTEST")
    click.echo("args passed:")
    click.echo("  AMOUNT -> {}".format(amount))
    click.echo("  ADDRESS -> {}".format(address))
    click.echo("  Confs -> {}".format(confirmations))

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
    """register a NAME, requires funds in wallet"""
    path = "/v1/names"
    payload = {'name': name}
    url = create_url(config,path)
    r = requests.post(url, headers=make_headers(config), json=payload)
    output(config, url, r)

# blockstack-cli name revoke
# https://blockstack.github.io/blockstack-core/#managing-names-revoke-name
@name.command()
@click.argument('NAME')
@pass_config    
def revoke(config, name):
    """revoke an owned NAME"""
    path = "/v1/names/{}".format(name)
    url = create_url(config,path)
    r = requests.delete(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli name transfer
# https://blockstack.github.io/blockstack-core/#managing-names-transfer-name
@name.command()
@click.argument('NAME')
@click.argument('OWNER')
@pass_config    
def transfer(config, name, owner):
    """transfer an owned NAME to OWNER"""
    path = "/v1/names/{}/owner".format(name)
    payload = {'owner': owner}
    url = create_url(config,path)
    r = requests.put(url, headers=make_headers(config), json=payload)
    output(config, url, r)

# blockstack-cli name set_zonefile
# https://blockstack.github.io/blockstack-core/#managing-names-set-zone-file
@name.command()
@click.argument('NAME')
@click.argument('ZONEFILE', type=click.File('rb'))
@pass_config    
def set_zonefile(config, name, zonefile):
    """set zonefile for NAME"""
    path = "/v1/names/{}/zonefile".format(name)
    payload = { 'zonefile': zonefile.read() }
    url = create_url(config,path)
    r = requests.put(url, headers=make_headers(config), json=payload)
    output(config, url, r)

# blockstack-cli name get_zonefile
# https://blockstack.github.io/blockstack-core/#managing-names-fetch-zone-file
@name.command()
@click.argument('NAME')
@pass_config    
def get_zonefile(config, name):
    """get zonefile for NAME"""
    path = "/v1/names/{}/zonefile".format(name)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli name get_page
# https://blockstack.github.io/blockstack-core/#name-querying-get-all-names
@name.command()
@click.argument('PAGE')
@pass_config
def get_page(config,page):
    """get a page from the list all blockstack names"""
    path = "/v1/names?page={}".format(page)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli name get
# https://blockstack.github.io/blockstack-core/#name-querying-get-name-info
@name.command()
@click.argument('NAME')
@pass_config
def get(config,name):
    """get details for a name"""
    path = "/v1/names/{}".format(name)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli name history
# https://blockstack.github.io/blockstack-core/#name-querying-name-history
@name.command()
@click.argument('NAME')
@pass_config
def history(config,name):
    """get the transfer history for a name"""
    path = "/v1/names/{}/history".format(name)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli name zonefile_history
# https://blockstack.github.io/blockstack-core/#name-querying-get-historical-zone-file
@name.command()
@click.argument('NAME')
@click.argument('ZONEFILEHASH')
@pass_config
def zonefile_history(config,name,zonefilehash):
    """zonefile_history name thing"""
    path = "/v1/names/{}/zonefile/{}".format(name,zonefilehash)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli name address
# https://blockstack.github.io/blockstack-core/#name-querying-get-names-owned-by-address
@name.command()
@click.argument('ADDRESS')
@click.option('--blockchain', default='bitcoin', help='blockchain to which address belongs. Currently only bitcoin is supported')
@pass_config
def address(config,address,blockchain):
    """address name thing"""
    path = "/v1/addresses/{}/{}".format(blockchain,address)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

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
    path = "/v1/prices/namespaces/{}".format(namespace)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli price name 
# https://blockstack.github.io/blockstack-core/#price-checks-get-name-price
@price.command()
@click.argument('name')
@pass_config
def name(config,name):
    """get the price for a name"""
    path = "/v1/prices/names/{}".format(name)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)


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
    path = "/v1/blockchains/{}/consensus".format(blockchain)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli blockchain get_pending
# https://blockstack.github.io/blockstack-core/#blockchain-operations-get-pending-transactions    
@blockchain.command()
@click.option('--blockchain', default='bitcoin', help='blockchain to which address belongs. Currently only bitcoin is supported')
@pass_config
def get_pending(config,blockchain):
    """get_pending transactions from connected blockchain node"""
    path = "/v1/blockchains/{}/pending".format(blockchain)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli blockchain get_utxo
# https://blockstack.github.io/blockstack-core/#blockchain-operations-get-unspent-outputs
@blockchain.command()
@click.option('--blockchain', default='bitcoin', help='blockchain to which address belongs. Currently only bitcoin is supported')
@click.argument('ADDRESS')
@pass_config
def get_utxo(config,blockchain,address):
    """get unspent transaction outputs from an ADDRESS"""
    path = "/v1/blockchains/{}/{}/unspent".format(blockchain,address)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli blockchain send_transaction
# https://blockstack.github.io/blockstack-core/#blockchain-operations-broadcast-transaction
@blockchain.command()
@click.option('--blockchain', default='bitcoin', help='blockchain to which address belongs. Currently only bitcoin is supported')
@click.argument('JSON', type=click.File('rb'))
@pass_config
def send_transaction(config,blockchain,json):
    """send a transaction to the underlying blockchain"""
    click.echo('NOT IMPLEMENTED YET\nSending transaction to the {} blockchain from file {}...'.format(blockchain,json))
    

###########################
# GROUP: GAIA
# blockstack-cli gaia
###########################
@cli.group()
@pass_config
def gaia(config):
    """these are gaia commands"""
    pass

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
    click.echo("NOT IMPLEMENTED YET, AWAITING STABLE GAIA API")
    
# blockstack-cli gaia store get
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-get-store-metadata
@store.command()
@click.argument("STORE")
@pass_config
def get(config,store):
    """retrieve STORE details"""
    click.echo("NOT IMPLEMENTED YET, AWAITING STABLE GAIA API")
    
# blockstack-cli gaia store delete
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-delete-store-
@store.command()
@click.argument("STORE")
@pass_config
def delete(config,store):
    """remove a STORE"""
    click.echo("NOT IMPLEMENTED YET, AWAITING STABLE GAIA API")

# blockstack-cli gaia inode 
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-get-inode-info
@gaia.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def inode(config,store,path):
    """get info about inode at PATH from STORE"""
    click.echo("NOT IMPLEMENTED YET, AWAITING STABLE GAIA API")
    
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
    click.echo("NOT IMPLEMENTED YET, AWAITING STABLE GAIA API")

# blockstack-cli gaia directory create
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-create-directory
@directory.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def create(config,store,path):
    """create directory at PATH from STORE"""
    click.echo("NOT IMPLEMENTED YET, AWAITING STABLE GAIA API")

# blockstack-cli gaia directory delete
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-delete-directory
@directory.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def delete(config,store,path):
    """delete directory at PATH from STORE"""
    click.echo("NOT IMPLEMENTED YET, AWAITING STABLE GAIA API")

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
    click.echo("NOT IMPLEMENTED YET, AWAITING STABLE GAIA API")
    
# blockstack-cli gaia file create
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-create-file
@file.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def create(config,store,path):
    """create file at given PATH from STORE"""
    click.echo("NOT IMPLEMENTED YET, AWAITING STABLE GAIA API")
    
# blockstack-cli gaia file update
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-update-file
@file.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def update(config,store,path):
    """update file at given PATH from STORE"""
    click.echo("NOT IMPLEMENTED YET, AWAITING STABLE GAIA API")
    
# blockstack-cli gaia file delete
# https://blockstack.github.io/blockstack-core/#gaia-endpoints-delete-file
@file.command()
@click.argument("STORE")
@click.argument("PATH")
@pass_config
def delete(config,store,path):
    """delete file at given PATH from STORE"""
    click.echo("NOT IMPLEMENTED YET, AWAITING STABLE GAIA API")


###########################
# GROUP: NAMESPACE
# blockstack-cli namespace
###########################
@cli.group()
@pass_config
def namespace(config):
    """these are namespace commands"""
    pass
    
# blockstack-cli namespace all
# https://blockstack.github.io/blockstack-core/#namespace-operations-get-all-namespaces
@namespace.command()
@pass_config
def all(config):
    """get a list of all namespaces"""
    path = "/v1/namespaces".format(blockchain,address)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

# blockstack-cli namespace names
# https://blockstack.github.io/blockstack-core/#namespace-operations-get-namespace-names
@namespace.command()
@click.option('-tld', default='id', help='top level domain to look for names in...')
@click.argument("PAGE")
@pass_config
def names(config,page,tld):
    """get a PAGE of names from a -tld"""
    path = "/v1/namespaces/{}/names?page={}".format(tld,page)
    url = create_url(config,path)
    r = requests.get(url, headers=make_headers(config))
    output(config, url, r)

