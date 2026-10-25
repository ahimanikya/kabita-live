export {validMonth} from './monthly-policy.mjs';
export function editorialDraft(entry,state,month=''){
 const messages={received:'Thank you for sharing your poem with Kabita Live. It has been received for editorial consideration.',shortlisted:'Your poem has been shortlisted for further consideration. This is not a final selection.',selected:`Your poem has been selected for Kabita Live.${month?` The planned issue month is ${month}.`:' We will confirm the issue month separately.'}`,declined:'Thank you for sharing your work. After consideration, we are unable to include this poem. We appreciate the opportunity to read it.'};
 if(!Object.hasOwn(messages,state))throw Error('Unknown decision');return {to:entry.email,subject:`Kabita Live — ${entry.title.replace(/[\r\n]/g,' ')}`,body:`Dear ${entry.name},\n\n${messages[state]}\n\nReference: ${entry.id}\n\nWarm regards,\nKabita Live editorial team\nkabitaliveweb@gmail.com`};
}
