package ccu.general;

public class StringUtils {
	public static int countChars(String getString, String replaceChar) {
		int charNum = 0;
		charNum = getString.length() - getString.replace(replaceChar, "").length();
		
		return charNum;
	}
}
