# -*- encoding: utf8 -*-
import	tools
import  cloudmgrws.tools
import  cloudmgrws.ssh_tools
import 	time

CHECK_SCREEN_COMMAND                            = 'check_screen'
SHUTDOWN_COMMAND                    		= 'shutdown'
SLEEP_COMMAND					= 'sleep'

checks = {
    CHECK_SCREEN_COMMAND                        : 'screen -ls | grep CLOUDMGRFTP',
    SHUTDOWN_COMMAND                        	: '''source $HOME/.bash_profile ; screen -S CLOUDMGRFTP -p 0 -X stuff $'\cC' ;''',
    SLEEP_COMMAND				: 'sleep 2',
}

@tools.topology_params
@cloudmgrws.tools.dynamic_parameters()
def shutdown( topology_params, function_params, ssh, response, *args, **kwargs ):

     return cloudmgrws.ssh_tools.process_steps(
         [
             # Verification de la presence du processus
             # Si le proceccus n'existe pas l'arret est annule
             { 
                 cloudmgrws.ssh_tools.STEP_NAME		: CHECK_SCREEN_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND	: checks[ CHECK_SCREEN_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS		: [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_PROCESS_NUMBER_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDOUT ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 1,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Process number incorrect (%s). Shutdown aborted.' % status,
                                                           },
							   {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Shutdown aborted.' % checks[ CHECK_SCREEN_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Shutdown aborted.',
                                                           },
                                                          ]
             },
             # Demande d'arret via une commande standard
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : SHUTDOWN_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : checks[ SHUTDOWN_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
							    cloudmgrws.ssh_tools.TEST_EXIT_ON_ERROR	: False,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Shutdown aborted.' % checks[ CHECK_SCREEN_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
							    cloudmgrws.ssh_tools.TEST_EXIT_ON_ERROR	: False,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Shutdown aborted.',
                                                           },
                                                          ]
             },
             # Attente avant test
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : SLEEP_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : checks[ SLEEP_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Shutdown aborted.' % checks[ CHECK_SCREEN_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Shutdown aborted.',
                                                           },
                                                          ]
             },
             # Test si le processus est mort
             # Si le processus n'est pas mort
             # les tests continuent
             {
                 cloudmgrws.ssh_tools.STEP_NAME         : CHECK_SCREEN_COMMAND,
                 cloudmgrws.ssh_tools.SHELL_COMMAND     : checks[ CHECK_SCREEN_COMMAND ].format( **function_params._asdict() ),
                 cloudmgrws.ssh_tools.TESTS             : [
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_PROCESS_NUMBER_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDOUT ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status <> 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Process number incorrect (%s). Shutdown aborted.' % status,
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.IS_RETURN_CODE_INCORRECT,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: result[ cloudmgrws.ssh_tools.RETURN_CODE ],
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status == 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Error executing %s. Shutdown aborted.' % checks[ CHECK_SCREEN_COMMAND ].format( **function_params._asdict() ),
                                                           },
                                                           {
                                                            cloudmgrws.ssh_tools.TEST_NAME              : cloudmgrws.ssh_tools.HAVE_STDERR,
                                                            cloudmgrws.ssh_tools.TEST_STATUS            : lambda result: len( result[ cloudmgrws.ssh_tools.STDERR ] ),
                                                            cloudmgrws.ssh_tools.TEST_IS_IN_ERROR       : lambda status: status > 0,
                                                            cloudmgrws.ssh_tools.TEST_ERROR_MESSAGE     : lambda status: 'Look at stderr. Shutdown aborted.',
                                                           },
                                                          ]
             },
         ],
         ssh,
         response,
     )     
