package ccu.general;

import java.util.ArrayList;

import ccu.command.MathParser;
import ccu.command.ServerOverride;
import ccu.command.Short_Execute;
import ccu.command.Short_Scoreboard;
import ccu.command.Short_Selector;
import ccu.mcfunction.FunctionNick;

public class StringUtils {
	public static int countChars(String getString, String replaceChar) {
		int charNum = 0;
		charNum = getString.length() - getString.replace(replaceChar, "").length();
		if (replaceChar.length() > 1) {
			charNum /= replaceChar.length();
		}

		return charNum;
	}

	public static String getWhiteSpace(String getString) {
		String returnString = null;
		returnString = getString.substring(0, StringUtils.countChars(getString, "\t"));

		return returnString;
	}

	public static ArrayList<String> skipLine(ArrayList<String> getArray, String getChar) {
		ArrayList<String> returnArray = new ArrayList<String>();
		String calcString = "";
		boolean skipLine = false;

		for (int i = 0; i < getArray.size(); i++) {

			skipLine = false;
			if (getArray.get(i).endsWith(getChar)) {
				skipLine = true;
			}

			if (skipLine == true) {
				if (calcString.isEmpty()) {
					calcString += getArray.get(i).substring(0, getArray.get(i).length() - 1);
				} else {

					// trims to get rid of any whitespace in the front of the string
					String testString = getArray.get(i).trim().substring(0, getArray.get(i).trim().length() - 1);
					if (testString.startsWith("CCU_COND_")) {
						testString = testString.substring(9);
					}
					calcString += testString;
				}

				// if the document ended
				if (i == getArray.size() - 1) {
					returnArray.add(calcString);
				}

			} else {
				if (calcString.isEmpty()) {
					returnArray.add(getArray.get(i));
				} else {
					String testString = getArray.get(i).trim().substring(0, getArray.get(i).trim().length());
					calcString += testString;
					returnArray.add(calcString);
					calcString = "";
				}
			}
		}
		return returnArray;
	}

	public static String generalParse(String getString) {
		String returnString = null;
		String calcString = null;
		returnString = getString + "";

		// parses SIN, COS, TAN, CALC
		returnString = MathParser.parseSecondaryStatements(returnString, getString);

		// scoreboard shortcuts
		calcString = Short_Scoreboard.getCommand(returnString);
		if (calcString != null) {
			returnString = calcString + "";
		}

		// execute shortcuts
		calcString = Short_Execute.getCommand(returnString);
		if (calcString != null) {
			returnString = calcString + "";
		}

		// selector shortcuts
		calcString = Short_Selector.getCommand(returnString);
		if (calcString != null) {
			returnString = calcString + "";
		}

		// function shortcuts
		calcString = FunctionNick.getCommand(returnString);
		if (calcString != null) {
			returnString = calcString + "";
		}

		// server override (adding 'minecraft:')
		calcString = ServerOverride.getCommand(returnString);
		if (ReadConfig.serverPlugins == true
				&& (ReadConfig.serverOverrideArray == null || ReadConfig.serverOverrideArray[0].equals("")) == false) {
			if (calcString != null) {
				returnString = calcString + "";
			}
		}

		return returnString;
	}
}
