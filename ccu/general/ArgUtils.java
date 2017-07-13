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

	public static void checkWhiteSpace(ArrayList<String> getArray, int tabNum, boolean isArray) {
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

			// check if it's any statement --> can be skipped
			for (String statement : ReadCCUFile.statementArray) {
				if ((i > 0) && getArray.get(i - 1).trim().startsWith(statement)) {
					tabNumCalc++;
					break;
				}
			}

			if (isArray == true) {
				// starting { 
				if (i == 1) {
					tabNumCalc++;
				}

				// break } {
				if ((i > 0) && getArray.get(i - 1).trim().startsWith("} {")) {
					tabNumCalc++;
				}
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

	public static void checkCoords(String getString, int coordType, String fullLineGet) {
		String[] calcCoords = null;

		if (coordType == 4) {

			// if it's empty, it's valid lol
			if (getString.isEmpty() == false) {
				calcCoords = getString.split(" ");
				
				// teleports can be 3, 4 or 5
				if (calcCoords.length == 3 || calcCoords.length == 4 || calcCoords.length == 5) {
					
					// checks whether it's a proper coordinate (while replacing ~ with 0 so it's a number)
					for (String coords : calcCoords) {
						if (NumberUtils.isNum(coords.replace("~", "0")) == false) {
							System.out.println("ERROR: Coordinates '" + getString + "' in line '" + fullLineGet
									+ "' are invalid (a coordinate can only contain '~' and numbers)");
							System.exit(0);
						}
					}
				} else {
					
					// not 3, 4 or 5 numbers
					System.out.println("ERROR: Coordinates '" + getString + "' in line '" + fullLineGet
							+ "' are invalid (it must contain 3, 4 or 5 numbers)");
					System.exit(0);
				}
			}
		}
		
		if (coordType == 5) {
			
			// regular coords can be 3 or 6
			if (calcCoords.length == 3 || calcCoords.length == 6) {
				
				// checks whether it's a proper coordinate (while replacing ~ with 0 so it's a number)
				for (String coords : calcCoords) {
					if (NumberUtils.isNum(coords.replace("~", "0")) == false) {
						System.out.println("ERROR: Coordinates '" + getString + "' in line '" + fullLineGet
								+ "' are invalid (a coordinate can only contain '~' and numbers)");
						System.exit(0);
					}
				}
			} else {
				
				// not 3 or 6 numbers
				System.out.println("ERROR: Coordinates '" + getString + "' in line '" + fullLineGet
						+ "' are invalid (it must contain 3 or 6 numbers)");
				System.exit(0);
			}
		}

	}
}
