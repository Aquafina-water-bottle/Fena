package ccu.general;

import ccu.command.ServerOverride;
import ccu.command.Short_Execute;
import ccu.command.Short_Scoreboard;
import ccu.command.Short_Selector;
import ccu.mcfunction.FunctionNick;

public class StringUtils {
	public static int countChars(String getString, String replaceChar) {
		int charNum = 0;
		charNum = getString.length() - getString.replace(replaceChar, "").length();
		
		return charNum;
	}
	
	public static String getWhiteSpace(String getString) {
		String returnString = null;
		returnString = getString.substring(0, StringUtils.countChars(getString, "\t"));
		
		return returnString;
	}
	
	public static String generalParse(String getString) {
		String returnString = null;
		String calcString = null;
		returnString = getString + "";
		
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
		
		// server override
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
