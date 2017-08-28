package ccu.general;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import ccu.command.MathParser;
import ccu.command.ServerOverride;
import ccu.command.Short_Execute;
import ccu.command.Short_Scoreboard;
import ccu.command.Short_Selector;

public class StringUtils {
	public static String removeParse(String getString) {

		// removes PARSE()
		String[] parseArray = null;
		String returnString = null;
		parseArray = StringUtils.parseInside(getString);
		if (parseArray != null) {
			
			returnString = parseArray[0] + parseArray[3] + parseArray[2];
			
			if (returnString.contains("PARSE(")) {
				returnString = removeParse(returnString);
			}
			
			return returnString;
		}
		
		return getString;
		
	}
	
	public static String[] parseInside(String getString) {
		String[] returnArray = new String[4];
		String begCalcString = null;
		String midCalcString = null;
		String endCalcString = null;
		String removeCalcString = null;

		String begTest = "PARSE(";
		String endTest = ")";

		if (getString.contains(begTest) && getString.contains(endTest)) {
			
			begCalcString = getString.substring(0, getString.indexOf(begTest));
			getString = getString.substring(getString.indexOf(begTest));
			midCalcString = getString.substring(0, getString.indexOf(endTest) + endTest.length());
			endCalcString = getString.substring(getString.indexOf(endTest) + endTest.length());
			midCalcString = midCalcString.replace("`","");
			
			while (true) {
				if (countChars(midCalcString, "(") > countChars(midCalcString, ")")) {
					int tempIndex = 0;
					if (endCalcString.contains(")") == false) {
						System.out.println(
								"ERROR: Brackets are not balanced within '" + midCalcString + "' in line '" + getString + "'");
						System.exit(0);
					}

					// substrings at second char from end, adds to mid and removes from end
					tempIndex = endCalcString.indexOf(endTest);
					midCalcString += endCalcString.substring(0, tempIndex + endTest.length());
					endCalcString = endCalcString.substring(tempIndex + endTest.length());

				} else {
					break;
				}

			}
			
			// remove PARSE( and )
			removeCalcString = midCalcString.substring(begTest.length(), midCalcString.length() - endTest.length());

			// checks for further PARSE() statements inside
			if (removeCalcString.contains(begTest)) {
				String[] calcArray = parseInside(removeCalcString);
				if (calcArray != null) {
					midCalcString = calcArray[0] + calcArray[1] + calcArray[2];
					removeCalcString = calcArray[0] + calcArray[3] + calcArray[2];
				}
			}
			
			// checks for further PARSE() statements to the right
			if (endCalcString.contains(begTest)) {
				String[] calcArray = parseInside(endCalcString);
				if (calcArray != null) {
					endCalcString = calcArray[0] + calcArray[1] + calcArray[2];
				}
			}

			returnArray[0] = begCalcString;
			returnArray[1] = midCalcString;
			returnArray[2] = endCalcString;
			returnArray[3] = removeCalcString;
			
			return returnArray;
		}

		return null;

	}
	
	public static String[] getInside(String getString, String additionalBeg, String firstChar, String secondChar, boolean throwError) {
		String[] returnArray = new String[4];
		String begCalcString = null;
		String midCalcString = null;
		String endCalcString = null;
		String removeCalcString = null;

		if (getString.contains(additionalBeg + firstChar) && getString.contains(secondChar)) {
			begCalcString = getString.substring(0, getString.indexOf(additionalBeg + firstChar));
			midCalcString = getString.substring(getString.indexOf(additionalBeg + firstChar),
					getString.indexOf(secondChar) + secondChar.length());
			endCalcString = getString.substring(getString.indexOf(secondChar) + secondChar.length());

			do {
				if (countChars(midCalcString, firstChar) > countChars(midCalcString, secondChar)) {
					int tempIndex = 0;
					if (endCalcString.contains(secondChar) == false) {
						if (throwError) {
							switch (firstChar) {
							case "(":
								System.out.println(
										"ERROR: Brackets are not balanced within '" + midCalcString + "' in line '" + getString + "'");
								break;

							case "[":
								System.out.println("ERROR: Square brackets are not balanced within '" + midCalcString + "' in line '"
										+ getString + "'");
								break;

							case "{":
								System.out.println("ERROR: Curly brackets are not balanced within '" + midCalcString + "' in line '"
										+ getString + "'");
								break;
							}
							System.exit(0);

						} else {
							return null;
						}
					}

					// substrings at second char from end, adds to mid and removes from end
					tempIndex = endCalcString.indexOf(secondChar);
					midCalcString += endCalcString.substring(0, tempIndex + secondChar.length());
					endCalcString = endCalcString.substring(tempIndex + secondChar.length());

				} else {
					break;
				}

			} while (true);

			removeCalcString = midCalcString.substring(additionalBeg.length() + firstChar.length(),
					midCalcString.length() - secondChar.length());

			returnArray[0] = begCalcString;
			returnArray[1] = midCalcString;
			returnArray[2] = endCalcString;
			returnArray[3] = removeCalcString;
			return returnArray;
		}

		return null;
	}

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

	public static Integer indexOfRegex(String text, String regex) {
		Pattern pattern = Pattern.compile(regex);
		Matcher matcher = pattern.matcher(text);
		// Check all occurrences
		while (matcher.find()) {
			return matcher.start();
		}
		return null;
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

		// function shortcuts - obsolete, will be done after all is parsed
		/*
		calcString = FunctionNick.getCommand(returnString);
		if (calcString != null) {
			returnString = calcString + "";
		}*/

		// server override (adding 'minecraft:')
		calcString = ServerOverride.getCommand(returnString);
		if (ReadConfig.serverPlugins == true
				&& (ReadConfig.serverOverrideArray == null || ReadConfig.serverOverrideArray[0].equals("")) == false) {
			if (calcString != null) {
				returnString = calcString + "";
			}
		}

		returnString = returnString.replace("`", "");
		return returnString;
	}
}
