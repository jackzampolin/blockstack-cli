import click
import requests
import blockstack

class Config(object):
    
    def __init__(self):
        self.host = 'node.blockstack.org:6264'
        self.directory = '~/.blockstack'

pass_config = click.make_pass_decorator(Config, ensure=True)

# GROUP: blockstack-cli
# blockstack-cli
@click.group()
@click.option('--host', default='node.blockstack.org:6264', help='blockstack api node to connect to ')
@click.option('--directory', default='~/.blockstack', help='directory for blockstack configuration and data files')
@pass_config
def cli(config, host, directory):
    """A command line interface for the blockstack network and local installations"""
    config.host = host
    config.directory = directory


# GROUP: NODE
# blockstack-cli node
@cli.group()
@pass_config
def node(config):
    """commands for conifguring and reaching blockstackd nodes"""
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
@node.command()
@pass_config
def methods(config):
    """print out blockstack_client methods"""
    click.echo(dir(blockstack.blockstack_client))
    
    
# GROUP: WALLET
# blockstack-cli wallet
@cli.group()
@pass_config
def wallet(config):
    """commands to perform operations on your blockstack wallet"""
    click.echo('blockstack-cli wallet')

# blockstack-cli wallet payment_address
@wallet.command()
@pass_config
def payment_address(config):
    """retrieve the payment_address for your blockstack wallet"""
    click.echo("blockstack wallet payment_address")

# blockstack-cli wallet owner_address
@wallet.command()
@pass_config
def owner_address(config):
    """retrieve the owner_address for your blockstack wallet"""
    click.echo("blockstack wallet owner_address")

# blockstack-cli wallet pub_key
@wallet.command()
@pass_config
def pub_key(config):
    """retrieve the pub_key for your blockstack wallet"""
    click.echo("blockstack wallet pub_key")

# blockstack-cli wallet set_key
@wallet.command()
@click.argument('KEY')
@pass_config
def set_key(config, key):
    """set a specific key to use"""
    click.echo("using wallet with key {}".format(key))

# blockstack-cli wallet balance
@wallet.command()
@click.option('--confirmations', default=6, help='number of confirmations to include transactions in wallet balance')
@pass_config
def balance(config, confirmations):
    """retrieve wallet balance"""
    click.echo("blockstack wallet balance")

# blockstack-cli wallet send
@wallet.command()
@click.option('--confirmations', default=6, help='number of confirmations to include transactions in wallet balance')
@click.option('--tx_only', is_flag=True, help='a flag?')
@click.argument('AMOUNT')
@click.argument('ADDRESS')
@pass_config
def send(config,amount,address,confirmations,tx_only):
    """send AMOUNT to ADDRESS..."""
    click.echo("sending {} to {} after {} confirmations...".format(amount, address, confirmations))


# GROUP: NAME
# blockstack-cli name
@cli.group()
@pass_config
def name(config):
    """commands for name operations"""
    pass

@name.command()
@click.argument('NAME')
@pass_config
def register(config, name):
    """register a NAME"""
    click.echo('register for {}'.format(name))

@name.command()
@click.argument('NAME')
@pass_config    
def revoke(config, name):
    """revoke NAME"""
    click.echo('revoke for {}'.format(name))

@name.command()
@click.argument('NAME')
@click.argument('OWNER')
@pass_config    
def transfer(config, name, owner):
    """transfer NAME to OWNER"""
    click.echo('transfer {} to {}'.format(name, owner))

@name.command()
@click.argument('NAME')
@pass_config    
def set_zonefile(config, name):
    """set zonefile for NAME"""
    click.echo('set_zonefile for {}'.format(name))

@name.command()
@click.argument('NAME')
@pass_config    
def get_zonefile(config, name):
    """get zonefile for NAME"""
    click.echo('get_zonefile for {}'.format(name))


# GROUP: PRICE
# blockstack-cli price
@cli.command()
@pass_config
def price(config):
    """these are pricing commands"""
    click.echo('Hello price')
    
@cli.command()
@pass_config
def blockchain(config):
    """these are blockchain commands"""
    click.echo('Hello blockchain')

@cli.command()
@pass_config
def gaia(config):
    """these are gaia commands"""
    click.echo('Hello gaia')

@cli.command()
@pass_config
def namespace(config):
    """these are namespace commands"""
    click.echo('Hello namespace')


