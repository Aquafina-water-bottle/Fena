package ccu.command;

import ccu.general.ReadConfig;

public class Short_Execute {
	private final static int STRING = 0;
	private final static int INT = 1;
	private final static int SELECTOR = 2;
	private final static int DATATAG = 3;
	private final static int COMMAND = 4;
	private final static int COORDS = 5;
	private final static int EXECUTE = 6;
	private final static int BLOCK = 7;

	public static String getCommand(String getString, int tabNum) {

		String getWhiteSpace = null;
		String shortcutCalc = null;
		String[] shortcutCalcArray = null;
		int[] shortcutTypeArray = null;
		String shortcutResultCalc = null;
		boolean shortcutDataTag = false;
		boolean changedLine = false;
		boolean useShortcut = true;

		// Execute shortcuts
		// NOTICE: Execute shortcuts will be IGNORED if found in data tags

		/* shortcutSelectorArray
		 * 0 = string
		 * 1 = int
		 * 2 = selector
		 * 3 = data tag
		 * 4 = command
		 * 5 = coords
		 * 6 = 'execute'
		 * 7 = block
		 * 
		 * data tags overrides all
		 */

		getWhiteSpace = getString.substring(0, tabNum);
		shortcutCalc = getString.substring(tabNum);
		shortcutCalcArray = shortcutCalc.split(" ");
		shortcutTypeArray = new int[shortcutCalcArray.length];
		for (int j = 0; j < shortcutCalcArray.length; j++) {

			// if it's a data tag --> 3 (DATATAG)
			if (shortcutCalcArray[j].startsWith("{")) {
				shortcutDataTag = true;
			}
			if (shortcutDataTag == true) {
				shortcutTypeArray[j] = DATATAG;
				continue;
			}

			// if it is a coord (aka contains '~') --> 5
			if (shortcutCalcArray[j].startsWith("~")) {
				shortcutTypeArray[j] = COORDS;
				continue;
			}

			// if it is 'execute' --> 6
			if (shortcutCalcArray[j].equals("execute")) {
				shortcutTypeArray[j] = EXECUTE;
				continue;
			}

			// if it's a number (as int) --> 1 (INT)
			try {
				Integer.parseInt(shortcutCalcArray[j]);
				shortcutTypeArray[j] = INT;
				continue;
			} catch (NumberFormatException e) {
			}

			// if it is a selector --> 2 (SELECTOR)
			for (String selectorGet : ReadConfig.selectorArray) {
				if (shortcutCalcArray[j].startsWith(selectorGet)) {
					shortcutTypeArray[j] = SELECTOR;
					break;
				}
			}

			// if it is a command --> 4
			for (String cmdGet : ReadConfig.minecraftCommandsArray) {
				if (shortcutCalcArray[j].startsWith(cmdGet)) {
					shortcutTypeArray[j] = COMMAND;
					break;
				}
			}
			/* Right now, whether it is a block or not doesn't matter
			for (String blockGet : ReadConfig.blockArray) {
				if (shortcutCalcArray[j].startsWith(blockGet)) {
					shortcutTypeArray[j] = BLOCK;
					break;
				}
			}*/
		}

		/*
		for (int j = 0; j < shortcutCalcArray.length; j++) {
			System.out.print(shortcutCalcArray[j] + " | " + shortcutTypeArray[j] + " | ");
		}
		System.out.println("");
		*/

		for (int j = 0; j < shortcutCalcArray.length; j++) {

			// If it ever hits a command or data tag, all hope is lost for the infamous execute shortcut
			// aka it can't be used anymore
			if (shortcutTypeArray[j] == COMMAND || shortcutTypeArray[j] == DATATAG) {
				useShortcut = false;
			}

			// if it can actually be used
			if (useShortcut == true) {

				// All execute shortcuts are based off of the singular selector
				if (shortcutTypeArray[j] == SELECTOR) {

					// if the future one is execute or selector or string or command
					// adds ~ ~ ~ in front
					if (j + 1 < shortcutCalcArray.length
							&& (shortcutTypeArray[j + 1] == EXECUTE || shortcutTypeArray[j + 1] == SELECTOR
									|| shortcutTypeArray[j + 1] == STRING || shortcutTypeArray[j + 1] == COMMAND)) {
						shortcutCalcArray[j] = shortcutCalcArray[j] + " ~ ~ ~";
						changedLine = true;
					}

					// if the previous one doesn't exist or if it doesn't have 'execute'
					// adds an execute behind
					if ((j >= 1 && shortcutTypeArray[j - 1] != EXECUTE) || j == 0) {
						shortcutCalcArray[j] = "execute " + shortcutCalcArray[j];
						changedLine = true;
					}
				}
			}
		}

		// gets the command for the next iteration to detect the execute detect by focusing on the block
		if (changedLine == true) {
			for (int j = 0; j < shortcutCalcArray.length; j++)
				if (j == 0) {
					shortcutResultCalc = shortcutCalcArray[j];
				} else {
					if (shortcutCalcArray[j].equals("") == false) {
						shortcutResultCalc += " " + shortcutCalcArray[j];
					}
				}
			shortcutCalc = shortcutResultCalc + "";
		}

		// reinitializing and reusing a few variables
		shortcutResultCalc = null;
		shortcutDataTag = false;
		useShortcut = true;

		shortcutCalcArray = shortcutCalc.split(" ");
		shortcutTypeArray = new int[shortcutCalcArray.length];
		for (int j = 0; j < shortcutCalcArray.length; j++) {

			// if it's a data tag --> 3 (DATATAG)
			if (shortcutCalcArray[j].startsWith("{")) {
				shortcutDataTag = true;
			}
			if (shortcutDataTag == true) {
				shortcutTypeArray[j] = DATATAG;
				continue;
			}

			// if it is a coord (aka contains '~') --> 5
			if (shortcutCalcArray[j].startsWith("~")) {
				shortcutTypeArray[j] = COORDS;
				continue;
			}

			// if it is 'execute' --> 6
			if (shortcutCalcArray[j].equals("execute")) {
				shortcutTypeArray[j] = EXECUTE;
				continue;
			}

			// if it's a number (as int) --> 1 (INT)
			try {
				Integer.parseInt(shortcutCalcArray[j]);
				shortcutTypeArray[j] = INT;
				continue;
			} catch (NumberFormatException e) {
			}

			// if it's equal to '*'
			if (shortcutCalcArray[j].equals("*")) {
				shortcutTypeArray[j] = INT;
				continue;
			}

			// if it is a selector --> 2 (SELECTOR)
			for (String selectorGet : ReadConfig.selectorArray) {
				if (shortcutCalcArray[j].startsWith(selectorGet)) {
					shortcutTypeArray[j] = SELECTOR;
					break;
				}
			}

			// if it is a command --> 4
			for (String cmdGet : ReadConfig.minecraftCommandsArray) {
				if (shortcutCalcArray[j].startsWith(cmdGet)) {
					shortcutTypeArray[j] = COMMAND;
					break;
				}
			}
			// if it is a block --> 7 (now whether it's a block matters a crap ton)
			for (String blockGet : ReadConfig.blockArray) {
				if (shortcutCalcArray[j].startsWith(blockGet)) {
					shortcutTypeArray[j] = BLOCK;
					break;
				}
			}
		}

		/*
		for (int j = 0; j < shortcutCalcArray.length; j++) {
			System.out.print(shortcutCalcArray[j] + " | " + shortcutTypeArray[j] + " | ");
		}
		System.out.println("");
		*/

		for (int j = 0; j < shortcutCalcArray.length; j++) {

			// If it ever hits a command or data tag, it can't be used anymore (still)
			if (shortcutTypeArray[j] == COMMAND || shortcutTypeArray[j] == DATATAG) {
				useShortcut = false;
			}

			// if it can actually be used
			if (useShortcut == true) {

				// All execute shortcuts are based off of the block
				if (shortcutTypeArray[j] == BLOCK) {

					// if the previous one is 'detect' - adds ~ ~ ~ 
					if (j >= 1 && shortcutCalcArray[j - 1].equals("detect") && shortcutTypeArray[j - 1] == STRING) {
						shortcutCalcArray[j] = "~ ~ ~ " + shortcutCalcArray[j];
						changedLine = true;
					}

					// if the future one is an int
					if (j + 1 < shortcutCalcArray.length && shortcutTypeArray[j + 1] == INT) {
						// if there are 4 numbers following - int and 3 coords/int
						// take 3 coordinates and moves it to the back of the block
						// also adds a 'detect' in behind of everything

						if (j + 4 < shortcutCalcArray.length
								&& ((shortcutTypeArray[j + 2] == INT || shortcutTypeArray[j + 2] == COORDS)
										&& (shortcutTypeArray[j + 3] == INT || shortcutTypeArray[j + 3] == COORDS)
										&& (shortcutTypeArray[j + 4] == INT || shortcutTypeArray[j + 4] == COORDS))) {
							shortcutCalcArray[j] = "detect " + shortcutCalcArray[j + 2] + " " + shortcutCalcArray[j + 3] + " "
									+ shortcutCalcArray[j + 4] + " " + shortcutCalcArray[j];
							shortcutCalcArray[j + 2] = "";
							shortcutCalcArray[j + 3] = "";
							shortcutCalcArray[j + 4] = "";
							changedLine = true;
						}

						// if there is just one number (if the 2nd if execute, selector or command)
						// and if there is a selector 4 before
						if (j + 2 < shortcutCalcArray.length && j >= 4 && shortcutTypeArray[j - 4] == SELECTOR
								&& ((shortcutTypeArray[j + 2] == EXECUTE) || shortcutTypeArray[j + 2] == SELECTOR
										|| shortcutTypeArray[j + 2] == COMMAND)) {
							// Adds ~ ~ ~ behind the block
							shortcutCalcArray[j] = "detect ~ ~ ~ " + shortcutCalcArray[j];
							changedLine = true;
						}
					}

					// if the future 3 are ints or coords and the 4th one is execute, selector or command
					if (j + 4 < shortcutCalcArray.length && ((shortcutTypeArray[j + 1] == INT || shortcutTypeArray[j + 1] == COORDS)
							&& (shortcutTypeArray[j + 2] == INT || shortcutTypeArray[j + 2] == COORDS)
							&& (shortcutTypeArray[j + 3] == INT || shortcutTypeArray[j + 3] == COORDS)
							&& (shortcutTypeArray[j + 4] == SELECTOR || shortcutTypeArray[j + 4] == EXECUTE
									|| shortcutTypeArray[j + 4] == COMMAND))) {
						// takes the coords, adds it behind the block and adds "detect" behind all
						// also adds "*" at the end
						shortcutCalcArray[j] = "detect " + shortcutCalcArray[j + 1] + " " + shortcutCalcArray[j + 2] + " "
								+ shortcutCalcArray[j + 3] + " " + shortcutCalcArray[j] + " *";
						shortcutCalcArray[j + 1] = "";
						shortcutCalcArray[j + 2] = "";
						shortcutCalcArray[j + 3] = "";
						changedLine = true;
					}

					// if the future one is execute, selector or command
					if (j + 1 < shortcutCalcArray.length && (shortcutTypeArray[j + 1] == EXECUTE
							|| shortcutTypeArray[j + 1] == SELECTOR || shortcutTypeArray[j + 1] == COMMAND)) {
						shortcutCalcArray[j] = "detect ~ ~ ~ " + shortcutCalcArray[j] + " *";
						changedLine = true;
					}

					/*
					// if the future one is execute or selector or string or command
					if (j + 1 < shortcutCalcArray.length
							&& (shortcutTypeArray[j + 1] == EXECUTE || shortcutTypeArray[j + 1] == SELECTOR
							|| shortcutTypeArray[j + 1] == STRING || shortcutTypeArray[j + 1] == COMMAND)) {
						shortcutCalcArray[j] = shortcutCalcArray[j] + " ~ ~ ~";
						changedLine = true;
					}
					
					// if the previous one doesn't exist or if it doesn't have 'execute'
					if ((j >= 1 && shortcutTypeArray[j - 1] != EXECUTE) || j == 0) {
						shortcutCalcArray[j] = "execute " + shortcutCalcArray[j];
						changedLine = true;
					}
					*/
				}
			}
		}

		// gets the command for the next iteration to detect the execute detect by focusing on the block
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
