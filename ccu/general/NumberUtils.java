package ccu.general;

public class NumberUtils {
	public static boolean isInt(String testInt) {
		if (testInt == null) {
			return false;
		} else {
			try {
				Integer.parseInt(testInt);
				return true;
			} catch (NumberFormatException e) {
				return false;
			}
		}
	}
	
	public static boolean isFloat(String testFloat) {
		if (testFloat == null) {
			return false;
		} else {
			try {
				Float.parseFloat(testFloat);
				return true;
			} catch (NumberFormatException e) {
				return false;
			}
		}
	}
}
