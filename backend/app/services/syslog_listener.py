import asyncio
import logging
from app.kafka.producer import producer

logger = logging.getLogger("ulpf.syslog")

class SyslogUDPServerProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport
        logger.info("Syslog UDP listener started on port 5140")

    def datagram_received(self, data: bytes, addr):
        try:
            message = data.decode("utf-8", errors="replace").strip()
            if message:
                producer.send_raw_event(raw_payload=message, source_id="src-syslog-live")
        except Exception as e:
            logger.error(f"Error handling syslog datagram: {e}")

async def start_syslog_server(host: str = "0.0.0.0", port: int = 5140):
    loop = asyncio.get_running_loop()
    try:
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: SyslogUDPServerProtocol(),
            local_addr=(host, port)
        )
        return transport
    except Exception as e:
        logger.warning(f"Could not bind Syslog UDP server to {host}:{port}: {e}")
        return None
