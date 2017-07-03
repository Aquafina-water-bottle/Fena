package ccu.block;

import java.util.ArrayList;

import ccu.command.Cmd_Group;

public class TempStringBuilder {
	public static ArrayList<String> tempCommandList = new ArrayList<String>();

	/*
	 * public static ArrayList<String[]> groupCommandsArray = new ArrayList<String[]>();
	 * public static ArrayList<Coordinates[]> groupCoordsArray = new ArrayList<Coordinates[]>();
	 * public static ArrayList<Integer[]> groupDirectionArray = new ArrayList<Integer[]>();
	 * public static ArrayList<Boolean[]> groupConditionalArray = new ArrayList<Boolean[]>();
	 * public static ArrayList<Integer> groupLineArray = new ArrayList<Integer>();
	 */

	// North, South, Sideways, Up, Down

	public static void getCommands() {
		int[] directionPosX = {5, 4, 3, 1, 0};
		int[] directionPosZ = {3, 2, 5, 1, 0};
		int[] directionNegX = {4, 5, 2, 1, 0};
		int[] directionNegZ = {2, 3, 4, 1, 0};
		int[] directionFinal = null;
		
		int dataValue = 0;
		tempCommandList.add("say CCU RCON in process");
		
		// checking direction
		if (GroupStructure.styleOptionXZ.equals("+X")) {
			directionFinal = directionPosX;
		}
		if (GroupStructure.styleOptionXZ.equals("+Z")) {
			directionFinal = directionPosZ;
		}
		if (GroupStructure.styleOptionXZ.equals("-X")) {
			directionFinal = directionNegX;
		}
		if (GroupStructure.styleOptionXZ.equals("-Z")) {
			directionFinal = directionNegZ;
		}
		
		
		for (int i = 0; i < GroupStructure.groupCommandsArray.size(); i++) {

			//System.out.println(CMD_Group.arrayGroupSave.get(i)[0] + " "
			//		+ Box.groupNameCoordArray[i].getString());

			for (int j = 0; j < GroupStructure.groupCommandsArray.get(i).length; j++) {
				StringBuilder cmd = new StringBuilder(100);
				cmd.append("setblock ");
				cmd.append(GroupStructure.groupCoordsArray.get(i)[j].getString());
				cmd.append(" ");
				if (j == 0) {
					cmd.append(Cmd_Group.arrayBlockTypeSave.get(i));
				} else {
					cmd.append("chain_command_block");
				}
				cmd.append(" ");

				dataValue = 0;

				if (GroupStructure.groupDirectionArray.get(i)[j].equals("NORTH")) {
					dataValue = directionFinal[0];
				}

				if (GroupStructure.groupDirectionArray.get(i)[j].equals("SOUTH")) {
					dataValue = directionFinal[1];
				}

				if (GroupStructure.groupDirectionArray.get(i)[j].equals("SIDEWAYS")) {
					dataValue = directionFinal[2];
				}

				if (GroupStructure.groupDirectionArray.get(i)[j].equals("UP")) {
					dataValue = directionFinal[3];
				}

				if (GroupStructure.groupDirectionArray.get(i)[j].equals("DOWN")) {
					dataValue = directionFinal[4];
				}

				if (GroupStructure.groupConditionalArray.get(i)[j] == true) {
					dataValue += 8;
				}
				cmd.append(dataValue);

				cmd.append(" replace {Command:\"");
				cmd.append(GroupStructure.groupCommandsArray.get(i)[j]);
				if (j == 0) {
					cmd.append("\",TrackOutput:0b,auto:0b}");
				} else {
					cmd.append("\",TrackOutput:0b,auto:1b}");
				}

				tempCommandList.add(cmd.toString());
				System.out.println(cmd);
			}
		}
	}
}
