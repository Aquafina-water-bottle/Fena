package ccu.rcon;

// Copied from CBP
// I have literally no idea what any of this is

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;

public class Transceiver {
	private Socket socket;
	private OutputStream os;
	private InputStream is;

	public Transceiver(String ip, int port, String pass) throws UnknownHostException, IOException {
		this.socket = new Socket(ip, port);
		this.is = this.socket.getInputStream();
		this.os = this.socket.getOutputStream();

		transceive(Packet.loginPacket(pass));
	}

	public Packet transceive(Packet packet) throws IOException {
		this.os.write(packet.getBytes());

		byte[] s = new byte[4];
		this.is.read(s);
		int size = Packet.asInt(s);
		if (size > 0) {
			byte[] buffer = new byte[size];
			this.is.read(buffer);
			return new Packet(buffer);
		}
		return null;
	}

	public String transceive(String cmd) throws IOException {
		Packet packet = transceive(Packet.commandPacket(cmd));
		if (packet == null) {
			return "ERROR";
		}
		return packet.message();
	}

	public ArrayList<String> transceive(ArrayList<String> cmds) throws IOException {
		ArrayList<String> responses = new ArrayList<String>();
		for (String cmd : cmds) {
			responses.add(transceive(cmd));
		}
		return responses;
	}

	public void close() throws IOException {
		this.socket.close();
	}
}
