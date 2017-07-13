package ccu.general;

import java.util.ArrayList;

import ccu.block.Box;
import ccu.block.GroupStructure;
import ccu.block.Setblock;
import ccu.command.MathParser;
import ccu.command.ReadCCUFile;
import ccu.command.Var_Options;
import ccu.mcfunction.WriteFile;
import ccu.rcon.MinecraftRcon;

public class Main {
	/* TODO
	 * For the program
	 * -Combiners - DONE
	 * -Scoreboard shortcuts - DONE
	 * -Execute shortcuts - DONE
	 * -Selector shortcuts - DONE
	 * -Definitions working with COORDS and TELE - DONE
	 * -Definitions within definitions - DONE
	 * -Usage of BRANCH via MFUNC - DONE
	 * -MFUNC nicknames - DONE
	 * -Server override using 'minecraft:' when detecing commands exist - DONE
	 * -Putting MFUNC into the parsed file - DONE
	 * -Skipping lines using ';' - DONE
	 * 
	 * -FUNC - DONE (now with proper future params)
	 * -IMPORT - DONE (without importing .dat files)
	 * -UNASSIGN - DONE (since arrays, team lists and objective lists aren't a thing yet)
	 * -LOOP - DONE (completely woot)
	 * -IF - DONE (completely WOOOT)
	 * -SIN COS TAN CALC - DONE WOOOOOOOOOT
	 * 
	 * -Repeated definitions - Already works apparently
	 * -Check whether commands exist - WILL NOT DO
	 * 
	 * -Better RCON usage - do when multiparse works
	 * -Combiner options using .mcfunction - do when multiparse works
	 * -Save coords option
	 * -Multiparse
	 * 
	 * General statements
	 * -INITIALIZE
	 * -ARRAY
	 * -OBJADD / OBJREV
	 * -TEAMADD / TEAMREV
	 * -FILE
	 * 
	 * Other
	 * -PARSE
	 * -Escaping using '`'
	 * -Escaping using '/' at the beginning of a line
	 * 
	 * Main thing is that all shortcuts will be done when parsing only at GROUP and MFUNC
	 * GROUP and MFUNC 
	 */

	// .replaceAll("^\\s+", "") = space to the left
	// .replaceAll("\\s+$", "") = space to the right

	public static void main(String[] args) {

		/*
		String ayylmao = null;
		
		ayylmao = "((3) * 4 ^ 2) (3 + 0) + -(1.5 - 0.5)";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "((3) * 4 ^ 2) (3 + 0) - (1.5 - 0.5)";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "230 2 ^ 0.9";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "3 10 + 0.7";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "(-10.5 + 0.5) (-115) * (1.1 + .9)";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "(-10) (-115) * (2.0)";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "(-10) (2 + (-115)) * (2.0)";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "-10 -115.0 * 0";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "-10 -115.0 * 1";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "100 5 - 5.0";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "256 1 / 2.0";
		MathParser.getLoopArray(ayylmao, ayylmao);
		*/

		/*
		ayylmao = "(3 * 4 ^ 2) (3 + 0) + -(2 - 1)";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "((3) * 4 ^ 2) (3 + 0) - (2 - 1)";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "2 2345678 ^ 2";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "3 10 + 2";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "(-11 + 1) (-115) * (1 + 1)";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "(-10) (-115) * (2)";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "(-10) (2 + (-115)) * (2)";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "-10 -115 * 0";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "-10 -115 * 1";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "100 5 - 5";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "256 1 / 2";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "1 1 + 5";
		MathParser.getLoopArray(ayylmao, ayylmao);
		
		ayylmao = "1 5 + 0";
		MathParser.getLoopArray(ayylmao, ayylmao);
		*/
		
		// String asdf = "this is a CALC(1 + SIN((1 - 2.0)) * (13 - 3)) asdf)";
		// MathParser.parseSecondaryStatements(asdf, asdf);
		
		

		
		// Reads the .ini file and gets the options
		ReadConfig.getConfigOptions();
		
		if (ReadConfig.regFilePath.toString().endsWith(".ccu") == false) {
			System.out.println("ERROR: File does not end with '.ccu'");
			System.exit(0);
		}
		
		// Reads the file stated in the .ini file
		ReadCCUFile ccuFile = new ReadCCUFile(ReadConfig.regFilePath);
		
		// Parses all CCU statements including defines
		ArrayList<String> getCommandsArray = ccuFile.checkCommands();
		
		// Checks if any options are left blank, and sets them to a default value if they are
		Var_Options.checkOptions();
		
		
		// for (String asdf : getCommandsArray) {
		//	System.out.println(asdf);
		// }
		
		// This pretty much only runs if something isn't encapsulated with MFUNC or GROUP
		if (getCommandsArray != null && getCommandsArray.isEmpty() == false) {
			
			System.out.println("\tERROR: Unnused commands in lines:");
			for (String line : getCommandsArray) {
				System.out.println("'" + line + "'");
			}
			System.exit(0);
		}
		
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
		// MinecraftRcon.useRcon();
		
	}
}
