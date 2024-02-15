class NodeException(Exception):
    """Raised when a node returns an error to a request."""
    pass

class NodeTimeoutException(Exception):
    """Raised when a request to a node times out."""
    pass

class TransactionTimeout(Exception):
    """Raised when the transaction didn't hit the chain within the provided timeout."""
    pass

class TransactionNotFound(Exception):
    """Raised when the transaction couldn't be found on chain."""
    pass

class NotAnApiNode(Exception):
    """The url passed to the constructor couldn't be detected as API node. This might be because you passed the rpc endpoint instead."""