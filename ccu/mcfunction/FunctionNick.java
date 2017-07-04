package ccu.mcfunction;

import ccu.command.Cmd_MFunc;

public class FunctionNick {

	public static String getCommand(String getString, int tabNum) {

		String getWhiteSpace = null;
		String shortcutCalc = null;
		String[] shortcutCalcArray = null;
		String shortcutResultCalc = null;
		boolean changedLine = false;

		getWhiteSpace = getString.substring(0, tabNum);
		shortcutCalc = getString.substring(tabNum);
		shortcutCalcArray = shortcutCalc.split(" ");
		for (int i = 0; i < shortcutCalcArray.length; i++) {

			// if it ends with 'function'
			if (shortcutCalcArray[i].endsWith("function")) {
				for (int j = 0; j < Cmd_MFunc.arrayMFuncNameSave.size(); j++) {
					System.out.println(shortcutCalcArray.length + " " + i);

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
					shortcutResultCalc = getWhiteSpace + shortcutCalcArray[j];
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
