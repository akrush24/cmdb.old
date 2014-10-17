#!/bin/sh
# Передаю директорию в качестве аргумента
inotifywait -mrq -e close_write -e moved_to -e create --format "%w%f" "$1" | while read "FILE"
do
if [ -d "$FILE" ]; then
chmod -R g+xw "$FILE"
chgrp cmdb "$FILE"
elif [ -f "$FILE" ]; then
chmod g+w "$FILE"
chgrp cmdb "$FILE"
fi
done
