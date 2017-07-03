package ccu.command;

public class Var_Func {
	/** Used for storing or reusing chunks of commands
	 * Avaliable parameters:
	 * GLOBAL
	 * 
	 * -ARGS is a special FUNC name meant for imported functions
	 * -CCU. is a special prefix to a FUNC name meant for imported functions
	 * {ARGS ACTIVATE CCU.xpNumber}:
	 * 
	 * How functions should work - No checkCommands() recurring loop
	 * Instead, just copies as is without any modification
	 * if there is a function call, it will check for params and whether it is isolated in a singular line
	 * then pastes in replacement of the line (aka returns function array) --> it should automatically do resetArray
	 * 
	 * To check for recurring functions with the combination of definitions and functions-
	 * -does a different constructor for ccuSubSetFile (add another string for function name)
	 * -If at any point a function call matches the function name, error + stop
	 * 
	 * FUNC {GLOBAL Func_Lmao}:
	 * 		say |0|
	 * 		FUNC GLOBAL {Func_Asdf}:
	 * 			say |0|
	 * 			say |0;1| first, |0| second
	 * 		Func_Asdf(3)
	 * Func_Lmao(1)
	 * Func_Asdf(5)
	 * 
	 * turns into
	 * 
	 * say |0|
	 * FUNC GLOBAL {Func_Asdf}:
	 * 		say |0|
	 * 		say |0;1| first, |0| second
	 * Func_Asdf(3)
	 * Func_Asdf(5)
	 * 
	 * turns into
	 * 
	 * say |0|
	 * say 3
	 * say |0| first, 3 second
	 * say 5
	 * say |0| first, 5 second
	 * 
	 * 
	 * turns into
	 * 
	 * say 1
	 * say 3
	 * say 1 first, 3 second
	 * say 5
	 * say 1 first, 5 second
	 */
}
