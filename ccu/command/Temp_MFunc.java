package ccu.command;

import java.util.ArrayList;

public class Temp_MFunc {
	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Temp_MFunc(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}
	
	public ArrayList<String> getArray() {
		ReadCCUFile ccuSubsetFile = new ReadCCUFile(this.arrayGet, tabNum);
		ArrayList<String> checkCommandsArray = ccuSubsetFile.checkCommands();
		if (checkCommandsArray != null && checkCommandsArray.isEmpty() == false) {
			this.arrayGet = checkCommandsArray;
		}
		
		ArrayList<String> arrayReturn = new ArrayList<String>();
		arrayReturn.add(this.fullLineGet);
		arrayReturn.addAll(this.arrayGet);
		
		return arrayReturn;
	}
}
