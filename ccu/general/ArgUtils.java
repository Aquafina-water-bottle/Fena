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

	public static void checkWhiteSpace(ArrayList<String> getArray, int tabNum) {
		String whitespaceCalc = null;
		int tabNumCalc = tabNum + 0;
		int countTabSpaces = 0;

		for (int i = 0; i < getArray.size(); i++) {

			whitespaceCalc = getArray.get(i).substring(0,
					(getArray.get(i).length() - getArray.get(i).replaceAll("^\\s+", "").length()));
			if (whitespaceCalc.contains(" ")) {
				System.out.println("ERROR: Line '" + getArray.get(i) + "' contains spaces instead of tab spaces");
				System.exit(0);
			}

			countTabSpaces = StringUtils.countChars(whitespaceCalc, "\t");

			// check if it's GROUP or MFUNC as they can be skipped
			if (getArray.get(i).trim().startsWith("GROUP") || getArray.get(i).trim().startsWith("MFUNC")) {
				tabNumCalc++;
				continue;
			}

			// check if it's been reduced
			if (countTabSpaces < tabNumCalc) {
				tabNumCalc = countTabSpaces + 0;
			}

			// if the number of tab spaces in the current line exceeds tab number calc or if it ever drops below the accepted tabnum
			if (countTabSpaces > tabNumCalc || countTabSpaces < tabNum) {
				System.out.println("ERROR: Line '" + getArray.get(i) + "' contains an incorrect number of tab spaces");
				System.exit(0);
			}
		}
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
