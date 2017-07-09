package ccu.command;

import ccu.general.ReadConfig;

public class Short_Scoreboard {
	private final static int STRING = 0;
	private final static int INT = 1;
	private final static int SELECTOR = 2;
	private final static int DATATAG = 3;
	
	public static String getCommand(String getString) {
		String shortcutCalc = null;
		String[] shortcutCalcArray = null;
		int[] shortcutTypeArray = null;
		String shortcutResultCalc = null;
		boolean shortcutDataTag = false;
		boolean containsScoreboard = false;
		boolean changedLine = false;

		// Scoreboard shortcut
		// NOTICE: Scoreboard shortcuts will be IGNORED if found in data tags
		// Also, scoreboard shortcuts can only happen once

		/* Scoreboard shortcuts (All selectors can be regular strings)
		 * scoreboard players add: @e[type=ArmorStand,RRStand] RRti + 1 {DisabledSlots:2096896}
		 * scoreboard players remove: @e[type=ArmorStand,RRStand] RRti - 1 {DisabledSlots:2096896}
		 * scoreboard players set: @e[type=ArmorStand,RRStand] RRti = 10 {DisabledSlots:2096896}
		 * scoreboard players operation: N/A - Define with ScOP
		 * scoreboard players test: @e[type=ArmorStand,RRStand] RRti ?
		 * scoreboard players test: @e[type=ArmorStand,RRStand] RRti ? 0 10
		 * scoreboard players reset: @e[type=ArmorStand,RRStand] reset RRti
		 * scoreboard players enable: @e[type=ArmorStand,RRStand] enable RRti
		 * scoreboard players tag @x add: @e[type=ArmorStand,RRStand] + RRTimer {Marker:1b}
		 * scoreboard players tag @x remove: @e[type=ArmorStand,RRStand] - RRTimer {Marker:1b}
		 * scoreboard teams join: RRd_y J> @e[type=ArmorStand,RRStand]
		 * scoreboard teams leave: RRd_y L> @e[type=ArmorStand,RRStand]
		 * scoreboard teams empty: RRd_y E>
		 */

		/* shortcutSelectorArray
		 * 0 = string
		 * 1 = int
		 * 2 = selector
		 * 3 = data tag
		 * 
		 * anything with a data tag, even with spaces will be 3 and not 0, 1 or 2
		 */

		shortcutCalc = getString.trim();
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

			// if it is 'scoreboard' - breaks because a scoreboard shortcut cannot be done here
			if (shortcutCalcArray[j].startsWith("scoreboard")) {
				containsScoreboard = true;
				break;
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

		}

		/*
		for (int j = 0; j < shortcutCalcArray.length; j++) {
			System.out.print(shortcutCalcArray[j] + " | " + shortcutTypeArray[j] + " | ");
		}
		System.out.println("");
		*/

		// Will do the scoreboard shortcut as long as 'scoreboard' is not present
		if (containsScoreboard == false) {
			for (int j = 0; j < shortcutCalcArray.length; j++) {

				// if it contains '+'
				if (shortcutCalcArray[j].equals("+") && shortcutTypeArray[j] == STRING) {

					// scoreboard players add
					if (j >= 2 && j + 1 < shortcutCalcArray.length
							&& (shortcutTypeArray[j - 2] == (STRING) || shortcutTypeArray[j - 2] == (SELECTOR))
							&& shortcutTypeArray[j - 1] == STRING && shortcutTypeArray[j + 1] == INT) {
						shortcutCalcArray[j - 2] = "scoreboard players add " + shortcutCalcArray[j - 2] + " "
								+ shortcutCalcArray[j - 1] + " " + shortcutCalcArray[j + 1];
						shortcutCalcArray[j - 1] = "";
						shortcutCalcArray[j - 0] = "";
						shortcutCalcArray[j + 1] = "";
						changedLine = true;
						break;
					}

					// scoreboard players tag name add
					if (j >= 1 && j + 1 < shortcutCalcArray.length && shortcutTypeArray[j - 1] == (STRING)
							|| shortcutTypeArray[j - 1] == (SELECTOR) && shortcutTypeArray[j + 1] == STRING) {
						shortcutCalcArray[j - 1] = "scoreboard players tag " + shortcutCalcArray[j - 1] + " add "
								+ shortcutCalcArray[j + 1];
						shortcutCalcArray[j - 0] = "";
						shortcutCalcArray[j + 1] = "";
						changedLine = true;
						break;
					}
				}

				// if it contains '-'
				if (shortcutCalcArray[j].equals("-") && shortcutTypeArray[j] == STRING) {

					// scoreboard players remove
					if (j >= 2 && j + 1 < shortcutCalcArray.length
							&& (shortcutTypeArray[j - 2] == (STRING) || shortcutTypeArray[j - 2] == (SELECTOR))
							&& shortcutTypeArray[j - 1] == STRING && shortcutTypeArray[j + 1] == INT) {
						shortcutCalcArray[j - 2] = "scoreboard players remove " + shortcutCalcArray[j - 2] + " "
								+ shortcutCalcArray[j - 1] + " " + shortcutCalcArray[j + 1];
						shortcutCalcArray[j - 1] = "";
						shortcutCalcArray[j - 0] = "";
						shortcutCalcArray[j + 1] = "";
						changedLine = true;
						break;
					}

					// scoreboard players tag name remove
					if (j >= 1 && j + 1 < shortcutCalcArray.length
							&& (shortcutTypeArray[j - 1] == (STRING) || shortcutTypeArray[j - 1] == (SELECTOR))
							&& shortcutTypeArray[j + 1] == STRING) {
						shortcutCalcArray[j - 1] = "scoreboard players tag " + shortcutCalcArray[j - 1] + " remove "
								+ shortcutCalcArray[j + 1];
						shortcutCalcArray[j - 0] = "";
						shortcutCalcArray[j + 1] = "";
						changedLine = true;
						break;
					}
				}

				// if it contains '='
				if (shortcutCalcArray[j].equals("=") && shortcutTypeArray[j] == STRING) {

					// scoreboard players set
					if (j >= 2 && j + 1 < shortcutCalcArray.length
							&& (shortcutTypeArray[j - 2] == (STRING) || shortcutTypeArray[j - 2] == (SELECTOR))
							&& shortcutTypeArray[j - 1] == STRING && shortcutTypeArray[j + 1] == INT) {
						shortcutCalcArray[j - 2] = "scoreboard players set " + shortcutCalcArray[j - 2] + " "
								+ shortcutCalcArray[j - 1] + " " + shortcutCalcArray[j + 1];
						shortcutCalcArray[j - 1] = "";
						shortcutCalcArray[j - 0] = "";
						shortcutCalcArray[j + 1] = "";
						changedLine = true;
						break;
					}
				}

				// if it contains '?'
				if (shortcutCalcArray[j].equals("?") && shortcutTypeArray[j] == STRING) {

					// scoreboard players test
					if (j >= 2 && j + 1 < shortcutCalcArray.length
							&& (shortcutTypeArray[j - 2] == (STRING) || shortcutTypeArray[j - 2] == (SELECTOR))
							&& shortcutTypeArray[j - 1] == STRING && shortcutTypeArray[j + 1] == INT) {
						shortcutCalcArray[j - 2] = "scoreboard players test " + shortcutCalcArray[j - 2] + " "
								+ shortcutCalcArray[j - 1] + " " + shortcutCalcArray[j + 1];
						shortcutCalcArray[j - 1] = "";
						shortcutCalcArray[j - 0] = "";
						shortcutCalcArray[j + 1] = "";
						changedLine = true;
						break;
					}
				}

				// if it contains 'reset' or 'enable'
				if (shortcutCalcArray[j].equals("reset")
						|| shortcutCalcArray[j].equals("enable") && shortcutTypeArray[j] == STRING) {

					// scoreboard players reset or enable
					if (j >= 1 && j + 1 < shortcutCalcArray.length
							&& (shortcutTypeArray[j - 1] == (STRING) || shortcutTypeArray[j - 1] == (SELECTOR))
							&& shortcutTypeArray[j + 1] == STRING) {
						shortcutCalcArray[j - 1] = "scoreboard players " + shortcutCalcArray[j] + " " + shortcutCalcArray[j - 1]
								+ " " + shortcutCalcArray[j + 1];
						shortcutCalcArray[j - 0] = "";
						shortcutCalcArray[j + 1] = "";
						changedLine = true;
						break;
					}
				}

				// if it contains 'J>'
				if (shortcutCalcArray[j].equals("J>") && shortcutTypeArray[j] == STRING) {

					// scoreboard teams join
					if (j >= 1 && j + 1 < shortcutCalcArray.length && shortcutTypeArray[j - 1] == STRING
							&& shortcutTypeArray[j + 1] == (STRING) || shortcutTypeArray[j + 1] == (SELECTOR)) {
						shortcutCalcArray[j - 1] = "scoreboard teams join " + shortcutCalcArray[j - 1] + " "
								+ shortcutCalcArray[j + 1];
						shortcutCalcArray[j - 0] = "";
						shortcutCalcArray[j + 1] = "";
						changedLine = true;
						break;
					}
				}

				// if it contains 'L>'
				if (shortcutCalcArray[j].equals("L>") && shortcutTypeArray[j] == STRING) {

					// scoreboard teams leave
					if (j >= 1 && j + 1 < shortcutCalcArray.length && shortcutTypeArray[j - 1] == STRING
							&& (shortcutTypeArray[j + 1] == (STRING) || shortcutTypeArray[j + 1] == (SELECTOR))) {
						shortcutCalcArray[j - 1] = "scoreboard teams leave " + shortcutCalcArray[j - 1] + " "
								+ shortcutCalcArray[j + 1];
						shortcutCalcArray[j - 0] = "";
						shortcutCalcArray[j + 1] = "";
						changedLine = true;
						break;
					}
				}

				// if it contains 'E>'
				if (shortcutCalcArray[j].equals("E>") && shortcutTypeArray[j] == STRING) {
					// scoreboard teams leave
					if (j >= 1 && shortcutTypeArray[j - 1] == STRING) {
						shortcutCalcArray[j - 1] = "scoreboard teams empty " + shortcutCalcArray[j - 1];
						shortcutCalcArray[j - 0] = "";
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
