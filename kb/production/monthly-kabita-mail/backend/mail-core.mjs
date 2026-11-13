// Server-only message preparation. Never accepts caller-supplied headers or templates.
import {createHash} from 'node:crypto';
export const SENDER = 'kabitaliveweb@gmail.com';
export const CALL = 'year-round';
const safeLine = (value, max) => typeof value === 'string' && value.trim() && value.length <= max && !/[\r\n\x00-\x1f\x7f]/.test(value);
export function mailbox(value) {
  if (!safeLine(value,254) || !/^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}$/.test(value)) throw new Error('Invalid recipient');
  return value;
}
// Gmail treats dots and +tags as the same recipient; do not allow quota evasion.
export function recipientKey(value) {
  let [local,domain]=mailbox(value).toLowerCase().split('@');
  if(domain==='googlemail.com') domain='gmail.com';
  if(domain==='gmail.com') local=local.split('+')[0].replaceAll('.','');
  return createHash('sha256').update(local+'@'+domain).digest('hex');
}
export function prepareMessages(id,entry,receipt) {
  if (!/^[A-Za-z0-9]{20}$/.test(id) || entry.callId!==CALL || entry.status!=='received' || !entry.uid || receipt.submissionId!==id) throw new Error('Unconfirmed submission');
  if(!safeLine(entry.name,120) || !safeLine(entry.title,200)) throw new Error('Invalid submission metadata');
  const email=mailbox(entry.email);
  const poet={id:id+'-poet',kind:'poet',to:email,recipientKey:recipientKey(email),subject:`Kabita Live — poem received: ${entry.title}`,text:`Dear ${entry.name},\n\nThank you for sharing “${entry.title}” with Kabita Live. We have received your poem for private editorial review.\n\nReference: ${id}\n\nThis confirms receipt, not selection for publication. The editors will choose an edition if your poem is selected. Please keep your own copy. You can reply to this email with questions, quoting your reference.\n\nWarm regards,\nKabita Live Editorial Team\n${SENDER}`};
  const organiser={id:id+'-organiser',kind:'organiser',to:SENDER,subject:`New Kabita Live submission · ${id}`,text:`A new private monthly entry is ready for review.\n\nReference: ${id}\nPoet: ${entry.name}\nTitle: ${entry.title}\nLanguage: ${entry.language}\n\nReview privately at https://kabitalive.com/monthly-review.html. Editors assign the issue month; nothing is published automatically.`};
  return [poet,organiser];
}
export function rawMessage(message) {
  mailbox(message.to);
  if(!safeLine(message.subject,300) || typeof message.text!=='string' || message.text.length>10000) throw new Error('Invalid message');
  const chunks=[];let chunk='';
  for(const char of message.subject){
    if(Buffer.byteLength(chunk+char)>42){chunks.push(chunk);chunk='';}
    chunk+=char;
  }
  if(chunk)chunks.push(chunk);
  const words=chunks.map(x=>`=?UTF-8?B?${Buffer.from(x).toString('base64')}?=`).join('\r\n ');
  const body=Buffer.from(message.text,'utf8').toString('base64').match(/.{1,76}/g).join('\r\n');
  return Buffer.from(`From: Kabita Live <${SENDER}>\r\nTo: ${message.to}\r\nReply-To: ${SENDER}\r\nSubject: ${words}\r\nMIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n${body}\r\n`).toString('base64url');
}
// Before a Gmail send, persist 'sending'. Never resend an uncertain attempt.
export function eligibleForSend(status) { return status==='queued'; }
export function sendOutcome({ok,status,messageId}) {
  if(ok && typeof messageId==='string' && messageId) return 'sent';
  if([400,401,403,404,429].includes(status)) return 'rejected';
  return 'uncertain'; // Timeout, transport loss, malformed success or server error.
}
