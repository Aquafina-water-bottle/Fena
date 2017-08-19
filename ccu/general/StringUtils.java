package ccu.general;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import ccu.command.MathParser;
import ccu.command.ServerOverride;
import ccu.command.Short_Execute;
import ccu.command.Short_Scoreboard;
import ccu.command.Short_Selector;

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
