package ccu.mcfunction;

import java.util.ArrayList;

import ccu.block.GroupStructure;
import ccu.block.Setblock;
import ccu.command.Cmd_MFunc;
import ccu.command.Var_Options;
import ccu.general.GeneralFile;

public class FunctionNick {
	
	private static void replaceFunctionNicks(ArrayList<String[]> arrayGet, int startInt) {
		for (int i = 0; i < arrayGet.size(); i++) {
			for (int j = 1; j < arrayGet.get(i).length; j++) {
				String calcString = getCommand(arrayGet.get(i)[j]);
				if (calcString != null) {
					arrayGet.get(i)[j] = calcString;
				}
			}
		}
	}
	
	private static void replaceFunctionNicksSingle(ArrayList<String> arrayGet, int startInt) {
		for (int i = 0; i < arrayGet.size(); i++) {
				String calcString = getCommand(arrayGet.get(i));
				if (calcString != null) {
					arrayGet.set(i, calcString);
				}
			}
	}

	public static void setFunctionNicks() {
		for (int i = 0; i < Cmd_MFunc.arrayMFuncSave.size(); i++) {
			String tempFileCalc = Var_Options.filePathFuncOption.toString().replace("\\", "/") + "/"
					+ Cmd_MFunc.arrayMFuncSave.get(i)[0];

			tempFileCalc = GeneralFile.checkFileExtension(tempFileCalc, ".mcfunction", true, true);
			System.out.println("File created: " + tempFileCalc);
			Cmd_MFunc.arrayMFuncSave.get(i)[0] = tempFileCalc;

			if (tempFileCalc.contains("/functions/")) {
				Cmd_MFunc.fileMFuncCommandSave.add(tempFileCalc.substring(0, tempFileCalc.length() - 11)
						.substring(tempFileCalc.indexOf("/functions/") + 11).replaceFirst("/", ":"));
			} else {
				System.out.println("ERROR: '" + tempFileCalc + "' is not in a 'functions' folder");
				System.exit(0);
			}
		}
		
		replaceFunctionNicks(GroupStructure.groupCommandsArray, 0);
		replaceFunctionNicks(Cmd_MFunc.arrayMFuncSave, 1);
		replaceFunctionNicksSingle(Setblock.initialCommands, 0);
		replaceFunctionNicksSingle(Setblock.finalCommands, 0);
	}

	public static String getCommand(String getString) {

		String shortcutCalc = null;
		String[] shortcutCalcArray = null;
		String shortcutResultCalc = null;
		boolean changedLine = false;

		shortcutCalc = getString.trim();
		shortcutCalcArray = shortcutCalc.split(" ");
		for (int i = 0; i < shortcutCalcArray.length; i++) {

			// if it ends with 'function'
			if (shortcutCalcArray[i].endsWith("function")) {
				for (int j = 0; j < Cmd_MFunc.arrayMFuncNameSave.size(); j++) {
					if (i + 1 < shortcutCalcArray.length && shortcutCalcArray[i + 1].equals(Cmd_MFunc.arrayMFuncNameSave.get(j))) {
						shortcutCalcArray[i + 1] = Cmd_MFunc.fileMFuncCommandSave.get(j);
						changedLine = true;
						break;
					}
				}
			}
		}

		if (changedLine == true) {
			for (int j = 0; j < shortcutCalcArray.length; j++)
				if (j == 0) {
					shortcutResultCalc = shortcutCalcArray[j];
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
