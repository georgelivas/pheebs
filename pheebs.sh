#/bin/sh

case $SHELL in
	*bash)
		ECHO='echo -e'
		;;
	*)
		ECHO='echo'
		;;
esac

white="\033[1;37m"
red="\033[1;31m"
green="\033[1;32m"
yellow="\033[1;33m"
blue="\033[1;34m"
transparent="\033[0m"

clear;
${ECHO} ""

sleep 0.02 && ${ECHO} "$blue "
sleep 0.02 && ${ECHO} "            ,,                         ,,                "
sleep 0.02 && ${ECHO} "\`7MM\"\"\"Mq.\`7MM                        *MM                "
sleep 0.02 && ${ECHO} "  MM   \`MM. MM                         MM                "
sleep 0.02 && ${ECHO} "  MM   ,M9  MMpMMMb.  .gP\"Ya   .gP\"Ya  MM,dMMb.  ,pP\"Ybd "
sleep 0.02 && ${ECHO} "  MMmmdM9   MM    MM ,M'   Yb ,M'   Yb MM    \`Mb 8I   \`\" "
sleep 0.02 && ${ECHO} "  MM        MM    MM 8M\"\"\"\"\"\" 8M\"\"\"\"\"\" MM     M8 \`YMMMa. "
sleep 0.02 && ${ECHO} "  MM        MM    MM YM.    , YM.    , MM.   ,M9 L.   I8 "
sleep 0.02 && ${ECHO} ".JMML.    .JMML  JMML.\`Mbmmd'  \`Mbmmd' P^YbmdP'  M9mmmP' "

${ECHO} "$transparent "

python3 detect.py