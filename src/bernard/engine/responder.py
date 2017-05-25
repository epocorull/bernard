# coding: utf-8
from typing import TYPE_CHECKING, Union, List
from bernard.layers import Stack, BaseLayer

if TYPE_CHECKING:
    from .platform import Platform
    from .request import Request


Layers = Union[Stack, List[BaseLayer]]


class ResponderError(Exception):
    """
    Base responder exception
    """


class UnacceptableStack(ResponderError):
    """
    The stack you're tryping to send can't be accepted by the platform
    """


class Responder(object):
    """
    The responder is the abstract object that allows to talk back to the
    conversation.

    If you implement a platform, you need to:

        - Overload the `__init__` in order to store whatever you need to reply
          (like the user ID...)
        - Implement the `_send_to_platform()` method, which will communicate
          with the platform in order to send the messages.
    """

    def __init__(self, platform: 'Platform'):
        self.platform = platform
        self._stacks = []  # type: List[Stack]

    def send(self, stack: Layers):
        """
        Add a message stack to the send list.
        """

        if not isinstance(stack, Stack):
            stack = Stack(stack)

        if not self.platform.accept(stack):
            raise UnacceptableStack('The platform does not allow "{}"'
                                    .format(stack.describe()))

        self._stacks.append(stack)

    def clear(self):
        """
        Reset the send list.
        """

        self._stacks = []

    async def _send_to_platform(self, stack: Stack):
        """
        Communicate with the platform to actually send the messages.
        """

        raise NotImplementedError

    async def flush(self):
        """
        Send all queued messages.
        """

        for stack in self._stacks:
            await self._send_to_platform(stack)

    def make_transition_register(self, request: 'Request'):
        """
        Use all underlying stacks to generate the next transition register.
        """

        register = {}

        for stack in self._stacks:
            register = stack.patch_register(register, request)

        return register