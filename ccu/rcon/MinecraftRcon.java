package ccu.rcon;

import java.io.IOException;
import java.util.ArrayList;

import ccu.block.TempStringBuilder;
import ccu.general.ReadConfig;

public class MinecraftRcon {
	public static ArrayList<String> rconArray = new ArrayList<String>();
	public static void useRcon() {
		if (ReadConfig.rconEnable) {
			if (ReadConfig.rconFunction == true) {
				// rconArray
			}
			try {
				Transceiver testRcon = new Transceiver(ReadConfig.rconIP, ReadConfig.rconPort.intValue(), ReadConfig.rconPassword);
				testRcon.transceive(TempStringBuilder.tempCommandList);
			} catch (IOException e) {
				System.out.println("ERROR: RCON failed");
				e.printStackTrace();
				System.exit(0);
			}
		}
	}
}
