package ccu.command;

import ccu.general.ReadConfig;

public class ServerOverride {
	public static String getCommand(String getString) {

		String shortcutCalc = null;
		String[] shortcutCalcArray = null;
		String shortcutResultCalc = null;
		boolean changedLine = false;
		boolean shortcutDataTag = false;

		shortcutCalc = getString.trim();
		shortcutCalcArray = shortcutCalc.split(" ");
		
		String testCond = "";
		if (shortcutCalcArray[0].startsWith("CCU_COND_")) {
			testCond = "CCU_COND_";
			shortcutCalcArray[0] = shortcutCalcArray[0].substring(9);
		}

		for (int j = 0; j < shortcutCalcArray.length; j++) {

			// if it's a data tag --> 3 (DATATAG)
			if (shortcutCalcArray[j].startsWith("{")) {
				shortcutDataTag = true;
			}
			
			for (String cmdGet : ReadConfig.minecraftCommandsArray) {
				if (j >= 1 && shortcutCalcArray[j - 1].equals(cmdGet)) {
					shortcutDataTag = true;
				}
			}
			
			if (shortcutDataTag == false) {
				for (String cmdGet : ReadConfig.serverOverrideArray) {
					if (shortcutCalcArray[j].equals(cmdGet)) {
						shortcutCalcArray[j] = "minecraft:" + shortcutCalcArray[j];
						changedLine = true;
						break;
					}
				}
			}
		}

		if (changedLine == true) {
			for (int j = 0; j < shortcutCalcArray.length; j++)
				if (j == 0) {
					shortcutResultCalc = testCond + shortcutCalcArray[j];
				} else {
					if (shortcutCalcArray[j].equals("") == false) {
						shortcutResultCalc += " " + shortcutCalcArray[j];
					}
				}
			return shortcutResultCalc;
		} else {
			return null;
		}
	}
}
