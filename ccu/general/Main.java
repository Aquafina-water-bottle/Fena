package ccu.general;

import java.util.ArrayList;

import ccu.block.Box;
import ccu.block.GroupStructure;
import ccu.block.Setblock;
import ccu.command.ReadCCUFile;
import ccu.command.Var_Options;
import ccu.mcfunction.WriteFile;
import ccu.rcon.MinecraftRcon;

public class Main {
	/* TODO - Goal is 3 to 4 per day
	 * For the program
	 * -Combiners - DONE
	 * -Better RCON usage
	 * -Usage of BRANCH via MFUNC and nicknames
	 * -Scoreboard shortcuts - DONE
	 * -Execute shortcuts - DONE
	 * -Selector shortcuts - DONE
	 * -Check whether commands exist
	 * -Server override using 'minecraft:' when detecing commands exist
	 * -Combiner options using .mcfunction
	 * -Save coords option
	 * -Definitions working with COORDS and TELE
	 * -Repeated definitions - Already works apparently
	 * -Definitions within definitions - DONE
	 * 
	 * 
	 * General statements
	 * -FUNC
	 * -ARRAY
	 * -IF
	 * -LOOP
	 * -IMPORT
	 * -UNASSIGN
	 * -OBJADD / OBJREV
	 * -TEAMADD / TEAMREV
	 * -FILE
	 * 
	 * Other
	 * -CALC
	 * -PARSE
	 * -SIN COS TAN
	 * -Escaping using '`'
	 * -Escaping using '/' at the beginning of a line
	 * -Skipping lines using ';'
	 */
	
	// .replaceAll("^\\s+", "") = space to the left
	// .replaceAll("\\s+$", "") = space to the right

	public static void main(String[] args) {
		// Reads the .ini file and gets the options
		ReadConfig.getConfigOptions();
		
		if (ReadConfig.regFilePath.toString().endsWith(".ccu") == false) {
			System.out.println("ERROR: File does not end with '.ccu'");
			System.exit(0);
		}

		// Reads the file stated in the .ini file
		ReadCCUFile ccuFile = new ReadCCUFile(ReadConfig.regFilePath);

		// Parses all CCU statements including defines
		ArrayList<String> checkLength = ccuFile.checkCommands();

		// This pretty much only runs if something isn't encapsulated with MFUNC or GROUP
		if (checkLength == null || checkLength.size() == 0) {
		} else {
			System.out.println("WARNING: Unnused commands starting from '" + checkLength.get(0) + "'");
		}

		// Checks if any options are left blank, and sets them to a default value if they are
		Var_Options.checkOptions();

		// Get the structures for each command block group
		GroupStructure.getGroupStructures();

		// Gets the full arrangement of structures
		Box.getBox();

		// Finalizes all commands with "setblock groupName" and "fill groupName"
		// Also writes the name_dat.ccu file
		Box.finalizeCoords();

		// Writes the mcfunction files since it's literally the easiest thing to do lmao
		WriteFile.writeMCFunction();

		// Writes the _commands, _parsed, and _combiner files
		Setblock.getCommands();

		// Writes the global Combiner file under globalCombinerFilePath

		// RCON
		MinecraftRcon.useRcon();
	}
}
