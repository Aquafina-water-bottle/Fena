package ccu.general;

import java.util.ArrayList;

import ccu.command.ReadCCUFile;

public class ArgUtils {
	public static ArrayList<String> checkCommands(ArrayList<String> getArray, int tabNum) {
		ArrayList<String> returnArray = getArray;

		ReadCCUFile ccuSubsetFile = new ReadCCUFile(getArray, tabNum);
		ArrayList<String> checkCommandsArray = ccuSubsetFile.checkCommands();
		if (checkCommandsArray != null && checkCommandsArray.isEmpty() == false) {
			returnArray = checkCommandsArray;
		}

		return returnArray;
	}

	public static String checkWhiteSpace(ArrayList<String> getArray, int tabNum) {
		String whitespaceCalc = null;

		for (int i = 0; i < getArray.size(); i++) {

			whitespaceCalc = getArray.get(i).substring(0,
					(getArray.get(i).length() - getArray.get(i).replaceAll("^\\s+", "").length()));
			if (whitespaceCalc.contains(" ")) {
				System.out.println("ERROR: Line '" + getArray.get(i) + "' contains spaces instead of tab spaces");
				System.exit(0);
			}

			if (whitespaceCalc.length() - whitespaceCalc.replace("\t", "").length() != tabNum) {
				System.out.println("ERROR: Line '" + getArray.get(i) + "' contains an incorrect number of tab spaces");
				System.exit(0);
			}
		}

		return whitespaceCalc;
	}
	
	public static String checkWhiteSpace(String getString, int tabNum) {
		String whitespaceCalc = null;

		whitespaceCalc = getString.substring(0, (getString.length() - getString.replaceAll("^\\s+", "").length()));
		if (whitespaceCalc.contains(" ")) {
			System.out.println("ERROR: Line '" + getString + "' contains spaces instead of tab spaces");
			System.exit(0);
		}

		if (whitespaceCalc.length() - whitespaceCalc.replace("\t", "").length() != tabNum) {
			System.out.println("ERROR: Line '" + getString + "' contains an incorrect number of tab spaces");
			System.exit(0);
		}

		return whitespaceCalc;
	}
}
