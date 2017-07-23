package ccu.rcon;

import java.io.IOException;
import java.util.ArrayList;

import ccu.block.Setblock;
import ccu.general.ReadConfig;

public class MinecraftRcon {
	public static ArrayList<String> rconArray = new ArrayList<String>();
	public static void useRcon() {
		if (ReadConfig.rconEnable) {
			/*if (ReadConfig.rconFunction == true) {
				// rconArray
			}*/
			try {
				Transceiver testRcon = new Transceiver(ReadConfig.rconIP, ReadConfig.rconPort.intValue(), ReadConfig.rconPassword);
				
				for (String writeCmd : Setblock.initialCommands) {
					rconArray.add(writeCmd);
				}
				for (String writeCmd : Setblock.setblockCommands) {
					rconArray.add(writeCmd);
				}
				for (String writeCmd : Setblock.finalCommands) {
					rconArray.add(writeCmd);
				}
				
				testRcon.transceive(rconArray);
				
			} catch (IOException e) {
				System.out.println("ERROR: RCON failed");
				e.printStackTrace();
				System.exit(0);
			}
		}
	}
}
