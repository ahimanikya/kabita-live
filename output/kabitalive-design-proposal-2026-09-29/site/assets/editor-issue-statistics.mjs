export function issueStatistics(issue,report){
 if(report?.available!==true)return {visits:null,shares:null};
 const paths=new Set([`issue-${issue.number}.html`,...(issue.poem_ids||[]).map(id=>`poem-${id}.html`)]);
 const rows=(report.rows||[]).filter(row=>paths.has(row.label));
 if(rows.some(row=>!Number.isSafeInteger(row.visits)||row.visits<0||!Number.isSafeInteger(row.shares)||row.shares<0))return {visits:null,shares:null};
 return rows.reduce((total,row)=>({visits:total.visits+row.visits,shares:total.shares+row.shares}),{visits:0,shares:0});
}
