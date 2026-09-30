import Foundation
import CoreGraphics
import CoreText
import AppKit
let dest = CommandLine.arguments[1]
var media = CGRect(x:0,y:0,width:595.28,height:841.89)
let consumer = CGDataConsumer(url:URL(fileURLWithPath:dest) as CFURL)!
let c = CGContext(consumer:consumer,mediaBox:&media,nil)!
let H=media.height
func color(_ hex:String)->CGColor { let n=UInt32(hex,radix:16)!;return CGColor(red:CGFloat((n>>16)&255)/255,green:CGFloat((n>>8)&255)/255,blue:CGFloat(n&255)/255,alpha:1) }
let ink=color("253A40"), rust=color("983E30"), muted=color("65665D"), paper=color("F6F1E7"), rule=color("D5CBB9")
func fill(_ x:CGFloat,_ top:CGFloat,_ w:CGFloat,_ h:CGFloat,_ col:CGColor){c.setFillColor(col);c.fill(CGRect(x:x,y:H-top-h,width:w,height:h))}
func text(_ s:String,_ x:CGFloat,_ top:CGFloat,_ size:CGFloat,_ font:String="Helvetica",_ col:CGColor?=nil){let f=CTFontCreateWithName(font as CFString,size,nil);let a=NSAttributedString(string:s,attributes:[NSAttributedString.Key(kCTFontAttributeName as String):f,NSAttributedString.Key(kCTForegroundColorAttributeName as String):col ?? ink]);let line=CTLineCreateWithAttributedString(a);c.textPosition=CGPoint(x:x,y:H-top-CTFontGetAscent(f));CTLineDraw(line,c)}
func para(_ s:String,_ x:CGFloat,_ top:CGFloat,_ w:CGFloat,_ h:CGFloat,_ size:CGFloat=10.3){let f=CTFontCreateWithName("Helvetica" as CFString,size,nil);let ps=NSMutableParagraphStyle();ps.lineSpacing=3;let a=NSAttributedString(string:s,attributes:[NSAttributedString.Key(kCTFontAttributeName as String):f,NSAttributedString.Key(kCTForegroundColorAttributeName as String):ink,.paragraphStyle:ps]);let fs=CTFramesetterCreateWithAttributedString(a);let path=CGPath(rect:CGRect(x:x,y:H-top-h,width:w,height:h),transform:nil);let frame=CTFramesetterCreateFrame(fs,CFRange(location:0,length:0),path,nil);let visible=CTFrameGetVisibleStringRange(frame);if visible.length < a.length{fatalError("Text overflow: \(s)")};CTFrameDraw(frame,c)}
func section(_ n:String,_ title:String,_ body:String,_ x:CGFloat,_ top:CGFloat){fill(x,top,249,1,rule);text(n+"  "+title,x,top+12,12,"Helvetica-Bold",rust);para(body,x,top+35,249,75)}
c.beginPDFPage(nil);fill(0,0,595.28,841.89,paper)
text("EDITOR'S BRANDING CHEAT SHEET",34,27,10,"Helvetica-Bold",rust)
text("Kabita Live",34,52,34,"Georgia")

text("ମାଟିର ମହକ। ମନର ସ୍ୱର।",34,118,21,"NotoSansOriya",rust)
text("Poetry is an echo, asking a shadow to dance.",34,159,12,"Georgia-Italic")
text("English masthead. Odia signature. Three languages, with equal care.",34,184,9.6,"Helvetica",muted)
section("01","NAME & LANGUAGES","Use Kabita Live alone in the masthead. Keep the Odia signature separate. Put Odia, Hindi and English filters beside the poem lists, outside the header. Preserve each poem’s original script.",34,212)
section("02","THE THEME ON EVERY PAGE","Use the Odia signature in the homepage hero, inner-page headers and every footer. Carry earth, warmth and human feeling through colour and small edge details. Keep art and texture outside poem text. Default to stillness.",311,212)
section("03","MAKE EACH COVER DISTINCT","Use a realistic artistic photograph or painterly-realistic image with one strong idea. Typeset the masthead separately. Keep issue/date and the signature legible. Record artist, rights and any AI use. Preserve historical originals.",34,336)
section("04","GIVE EACH WRITER A HOME","Preferred name and native script; approved portrait and biography; all contributions grouped by year/issue. Link every byline to the writer. Never invent a biography, publication count or social account.",311,336)
section("05","TYPE & COLOUR","Source Serif 4: English masthead. Noto Serif Oriya: Odia; Noto Serif Devanagari: Hindi. Menu 17 px; filters 16 px; targets 48 px. Poems 24 px desktop / 22 px mobile. Keep line breaks and natural script spacing.",34,460)
section("06","SHARE WITH THE CREDIT","Every shared piece keeps its full title, writer and original link. Link card: 1200 x 630. Square: 1080 x 1080. Story: 1080 x 1920, separately composed. Use excerpts only when approved. Never claim a post was sent.",311,460)
let swatches:[(String,String)] = [("Paper","F6F1E7"),("Ink","253A40"),("Indigo","263D4B"),("Red earth","983E30"),("Muted","65665D"),("Pale paper","EEE7D9")]
for (i,s) in swatches.enumerated(){let x=34+CGFloat(i)*89;fill(x,589,79,27,color(s.1));c.setStrokeColor(rule);c.stroke(CGRect(x:x,y:H-589-27,width:79,height:27));text(s.0,x,623,8.6,"Helvetica-Bold");text("#"+s.1,x,636,8.4,"Helvetica",muted)}
fill(34,669,527,1,rule)
text("BEFORE EACH ISSUE GOES LIVE",34,682,11,"Helvetica-Bold",rust)
para("Check: English name + Odia signature; all three languages; original verse + bylines; working writer and issue links; unique credited cover; readable mobile layout; correct sharing preview; complete archive records.",34,704,527,44,10.5)
text("Same masthead. A fresh cover. The poet's voice intact.",34,767,15,"Georgia")
text("Working editorial standard | 29 September 2026 | Companion: the visual branding guide",34,808,8,"Helvetica",muted)
c.endPDFPage();c.closePDF();print(dest)
