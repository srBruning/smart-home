# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import atuadores_pb2 as atuadores__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in atuadores_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ArCondicionadoStub(object):
    """Serviço para o Ar-Condicionado
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.LigarArCondicionado = channel.unary_unary(
                '/atuadores.ArCondicionado/LigarArCondicionado',
                request_serializer=atuadores__pb2.ComandoVazio.SerializeToString,
                response_deserializer=atuadores__pb2.RespostaAtuador.FromString,
                _registered_method=True)
        self.DesligarArCondicionado = channel.unary_unary(
                '/atuadores.ArCondicionado/DesligarArCondicionado',
                request_serializer=atuadores__pb2.ComandoVazio.SerializeToString,
                response_deserializer=atuadores__pb2.RespostaAtuador.FromString,
                _registered_method=True)
        self.SetTemperatura = channel.unary_unary(
                '/atuadores.ArCondicionado/SetTemperatura',
                request_serializer=atuadores__pb2.TemperaturaAtuador.SerializeToString,
                response_deserializer=atuadores__pb2.RespostaAtuador.FromString,
                _registered_method=True)
        self.GetTemperatura = channel.unary_unary(
                '/atuadores.ArCondicionado/GetTemperatura',
                request_serializer=atuadores__pb2.ComandoVazio.SerializeToString,
                response_deserializer=atuadores__pb2.EstadoTemperaturaAtuador.FromString,
                _registered_method=True)


class ArCondicionadoServicer(object):
    """Serviço para o Ar-Condicionado
    """

    def LigarArCondicionado(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DesligarArCondicionado(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetTemperatura(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTemperatura(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ArCondicionadoServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'LigarArCondicionado': grpc.unary_unary_rpc_method_handler(
                    servicer.LigarArCondicionado,
                    request_deserializer=atuadores__pb2.ComandoVazio.FromString,
                    response_serializer=atuadores__pb2.RespostaAtuador.SerializeToString,
            ),
            'DesligarArCondicionado': grpc.unary_unary_rpc_method_handler(
                    servicer.DesligarArCondicionado,
                    request_deserializer=atuadores__pb2.ComandoVazio.FromString,
                    response_serializer=atuadores__pb2.RespostaAtuador.SerializeToString,
            ),
            'SetTemperatura': grpc.unary_unary_rpc_method_handler(
                    servicer.SetTemperatura,
                    request_deserializer=atuadores__pb2.TemperaturaAtuador.FromString,
                    response_serializer=atuadores__pb2.RespostaAtuador.SerializeToString,
            ),
            'GetTemperatura': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTemperatura,
                    request_deserializer=atuadores__pb2.ComandoVazio.FromString,
                    response_serializer=atuadores__pb2.EstadoTemperaturaAtuador.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'atuadores.ArCondicionado', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('atuadores.ArCondicionado', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ArCondicionado(object):
    """Serviço para o Ar-Condicionado
    """

    @staticmethod
    def LigarArCondicionado(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/atuadores.ArCondicionado/LigarArCondicionado',
            atuadores__pb2.ComandoVazio.SerializeToString,
            atuadores__pb2.RespostaAtuador.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DesligarArCondicionado(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/atuadores.ArCondicionado/DesligarArCondicionado',
            atuadores__pb2.ComandoVazio.SerializeToString,
            atuadores__pb2.RespostaAtuador.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SetTemperatura(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/atuadores.ArCondicionado/SetTemperatura',
            atuadores__pb2.TemperaturaAtuador.SerializeToString,
            atuadores__pb2.RespostaAtuador.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetTemperatura(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/atuadores.ArCondicionado/GetTemperatura',
            atuadores__pb2.ComandoVazio.SerializeToString,
            atuadores__pb2.EstadoTemperaturaAtuador.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class LampadaStub(object):
    """Serviço para a Lâmpada
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.LigarLampada = channel.unary_unary(
                '/atuadores.Lampada/LigarLampada',
                request_serializer=atuadores__pb2.ComandoVazio.SerializeToString,
                response_deserializer=atuadores__pb2.RespostaAtuador.FromString,
                _registered_method=True)
        self.DesligarLampada = channel.unary_unary(
                '/atuadores.Lampada/DesligarLampada',
                request_serializer=atuadores__pb2.ComandoVazio.SerializeToString,
                response_deserializer=atuadores__pb2.RespostaAtuador.FromString,
                _registered_method=True)
        self.GetEstadoLampada = channel.unary_unary(
                '/atuadores.Lampada/GetEstadoLampada',
                request_serializer=atuadores__pb2.ComandoVazio.SerializeToString,
                response_deserializer=atuadores__pb2.EstadoAtuador.FromString,
                _registered_method=True)


class LampadaServicer(object):
    """Serviço para a Lâmpada
    """

    def LigarLampada(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DesligarLampada(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEstadoLampada(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LampadaServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'LigarLampada': grpc.unary_unary_rpc_method_handler(
                    servicer.LigarLampada,
                    request_deserializer=atuadores__pb2.ComandoVazio.FromString,
                    response_serializer=atuadores__pb2.RespostaAtuador.SerializeToString,
            ),
            'DesligarLampada': grpc.unary_unary_rpc_method_handler(
                    servicer.DesligarLampada,
                    request_deserializer=atuadores__pb2.ComandoVazio.FromString,
                    response_serializer=atuadores__pb2.RespostaAtuador.SerializeToString,
            ),
            'GetEstadoLampada': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEstadoLampada,
                    request_deserializer=atuadores__pb2.ComandoVazio.FromString,
                    response_serializer=atuadores__pb2.EstadoAtuador.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'atuadores.Lampada', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('atuadores.Lampada', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Lampada(object):
    """Serviço para a Lâmpada
    """

    @staticmethod
    def LigarLampada(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/atuadores.Lampada/LigarLampada',
            atuadores__pb2.ComandoVazio.SerializeToString,
            atuadores__pb2.RespostaAtuador.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DesligarLampada(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/atuadores.Lampada/DesligarLampada',
            atuadores__pb2.ComandoVazio.SerializeToString,
            atuadores__pb2.RespostaAtuador.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetEstadoLampada(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/atuadores.Lampada/GetEstadoLampada',
            atuadores__pb2.ComandoVazio.SerializeToString,
            atuadores__pb2.EstadoAtuador.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class ControleIncendioStub(object):
    """Serviço para o Sistema de Controle de Incêndio
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AtivarControleIncendio = channel.unary_unary(
                '/atuadores.ControleIncendio/AtivarControleIncendio',
                request_serializer=atuadores__pb2.ComandoVazio.SerializeToString,
                response_deserializer=atuadores__pb2.RespostaAtuador.FromString,
                _registered_method=True)
        self.DesativarControleIncendio = channel.unary_unary(
                '/atuadores.ControleIncendio/DesativarControleIncendio',
                request_serializer=atuadores__pb2.ComandoVazio.SerializeToString,
                response_deserializer=atuadores__pb2.RespostaAtuador.FromString,
                _registered_method=True)
        self.GetEstadoControleIncendio = channel.unary_unary(
                '/atuadores.ControleIncendio/GetEstadoControleIncendio',
                request_serializer=atuadores__pb2.ComandoVazio.SerializeToString,
                response_deserializer=atuadores__pb2.EstadoAtuador.FromString,
                _registered_method=True)


class ControleIncendioServicer(object):
    """Serviço para o Sistema de Controle de Incêndio
    """

    def AtivarControleIncendio(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DesativarControleIncendio(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEstadoControleIncendio(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ControleIncendioServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AtivarControleIncendio': grpc.unary_unary_rpc_method_handler(
                    servicer.AtivarControleIncendio,
                    request_deserializer=atuadores__pb2.ComandoVazio.FromString,
                    response_serializer=atuadores__pb2.RespostaAtuador.SerializeToString,
            ),
            'DesativarControleIncendio': grpc.unary_unary_rpc_method_handler(
                    servicer.DesativarControleIncendio,
                    request_deserializer=atuadores__pb2.ComandoVazio.FromString,
                    response_serializer=atuadores__pb2.RespostaAtuador.SerializeToString,
            ),
            'GetEstadoControleIncendio': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEstadoControleIncendio,
                    request_deserializer=atuadores__pb2.ComandoVazio.FromString,
                    response_serializer=atuadores__pb2.EstadoAtuador.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'atuadores.ControleIncendio', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('atuadores.ControleIncendio', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ControleIncendio(object):
    """Serviço para o Sistema de Controle de Incêndio
    """

    @staticmethod
    def AtivarControleIncendio(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/atuadores.ControleIncendio/AtivarControleIncendio',
            atuadores__pb2.ComandoVazio.SerializeToString,
            atuadores__pb2.RespostaAtuador.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DesativarControleIncendio(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/atuadores.ControleIncendio/DesativarControleIncendio',
            atuadores__pb2.ComandoVazio.SerializeToString,
            atuadores__pb2.RespostaAtuador.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetEstadoControleIncendio(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/atuadores.ControleIncendio/GetEstadoControleIncendio',
            atuadores__pb2.ComandoVazio.SerializeToString,
            atuadores__pb2.EstadoAtuador.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
