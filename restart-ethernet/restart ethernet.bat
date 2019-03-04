@echo on
netsh interface set interface "Local Area Connection" DISABLED
timeout /t 2
netsh interface set interface "Local Area Connection" ENABLED