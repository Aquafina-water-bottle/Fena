package ccu.rcon;

// Copied from CBP
// I have literally no idea what any of this is

public class Packet {
	private static int nextID = 0;
	private int requestID;
	private int type;
	private byte[] payload;

	public Packet() {
		this(0, -1, new byte[0]);
	}

	public Packet(int requestID, int type, byte[] payload) {
		this.requestID = requestID;
		this.type = type;
		this.payload = payload;
	}

	public Packet(byte[] message) {
		int i = 0;
		this.requestID = asInt(new byte[] {message[(i + 0)], message[(i + 1)], message[(i + 2)], message[(i + 3)]});
		this.type = asInt(new byte[] {message[(i + 4)], message[(i + 5)], message[(i + 6)], message[(i + 7)]});
		this.payload = new byte[message.length - 10];
		for (int j = 0; j < this.payload.length; j++) {
			this.payload[j] = message[(i + 8 + j)];
		}
	}

	/*public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append("ID:\n");
		sb.append(this.requestID);
		sb.append("\nType:\n");
		sb.append(this.type);
		sb.append("\nMessage:\n");
		sb.append(new String(this.payload));
		return sb.toString();
	}*/

	public String message() {
		return new String(this.payload);
	}

	public byte[] getBytes() {
		byte[] message = new byte[4 + getLength()];

		byte[] id = asByteArray(this.requestID);
		byte[] type = asByteArray(this.type);

		int i = 0;

		byte[] length = asByteArray(getLength());
		for (int j = 0; j < length.length; j++) {
			message[(i++)] = length[j];
		}
		for (int j = 0; j < id.length; j++) {
			message[(i++)] = id[j];
		}
		for (int j = 0; j < type.length; j++) {
			message[(i++)] = type[j];
		}
		for (int j = 0; j < this.payload.length; j++) {
			message[(i++)] = this.payload[j];
		}
		for (int j = 0; j < 2; j++) {
			message[(i++)] = 0;
		}
		return message;
	}

	public int getLength() {
		return 8 + this.payload.length + 2;
	}

	public static byte[] asByteArray(int value) {
		byte[] array = new byte[4];
		for (int i = 0; i < array.length; i++) {
			array[i] = ((byte) (value >> i * 8));
		}
		return array;
	}

	public static int asInt(byte[] array) {
		int value = 0;
		for (int i = 0; i < array.length; i++) {
			value = (int) (value | Byte.toUnsignedLong(array[i]) << i * 8);
		}
		return value;
	}

	public static Packet loginPacket(String pass) {
		Packet packet = new Packet(nextID++, 3, pass.getBytes());

		return packet;
	}

	public static Packet commandPacket(String command) {
		Packet packet = new Packet(nextID++, 2, command.getBytes());

		return packet;
	}
}
