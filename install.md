Running the backend services: 

`bash
runmaxit
`

runmaxit is saved in .bashrc and is currently 

`bash
alias runmaxit="(cd /workspaces/maxit_sales_bot/backend && python -m conversation_service.main --framework langgraph --user_id u1001 --query 'How does Seagate compare on profitability?' --save_graph no)
`

Connect to postgres via plsql: 
Application DB
`psql -h localhost -U maxit_user -d app_db` 

OpenWebUI DB
`psql -h localhost -U webui -d openwebui -p 5433`