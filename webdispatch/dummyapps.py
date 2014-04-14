""" dummy applications for testing paste.app_factory"""
from .testing import DummyApp

greeting = DummyApp([b'Hello'])
bye = DummyApp([b'bye'])
