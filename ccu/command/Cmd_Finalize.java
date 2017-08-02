package ccu.command;

import java.util.ArrayList;

import ccu.block.Setblock;
import ccu.general.ArgUtils;
import ccu.general.GeneralFile;
import ccu.general.StringUtils;

public class Cmd_Finalize {
	private ArrayList<String> arrayGet = new ArrayList<String>();
	private int tabNum;
	private String fullLineGet;

	public Cmd_Finalize(ArrayList<String> arrayGet, int tabNumGet, String fullLineGet) {
		this.arrayGet = arrayGet;
		this.tabNum = tabNumGet;
		this.fullLineGet = fullLineGet;
	}

	public ArrayList<String> getArray() {
		/** Just puts commands at the end without actually setting the command blocks
		 */

		// checkCommands
		ArgUtils.checkCommands(this.arrayGet, tabNum);

		// Check tab spaces
		ArgUtils.checkWhiteSpace(this.arrayGet, this.tabNum, false);

		// Removes "FINALIZE " and isolates for the arguments with brackets
		String statementEncase = this.fullLineGet.replaceFirst("FINALIZE", "").replaceAll("^\\s+", "");
		if (statementEncase.endsWith(":")) {

			this.arrayGet = GeneralFile.combineLine(this.arrayGet, ";");
			for (String cmd : this.arrayGet) {
				Setblock.finalCommands.add(StringUtils.generalParse(cmd.trim()));
			}

		} else {
			System.out.println("ERROR: Incorrect syntax at '" + this.fullLineGet + "'");
			System.exit(0);
		}

		// should always return null
		return null;
	}
}
