import Foundation
import CoreGraphics
import CoreText
import AppKit
let dest = CommandLine.arguments[1]
let sourceRoot=URL(fileURLWithPath:#filePath).deletingLastPathComponent().deletingLastPathComponent()
let odiaURL=sourceRoot.appendingPathComponent("site/assets/fonts/NotoSerifOriya-Variable.ttf")
var fontError: Unmanaged<CFError>?
guard CTFontManagerRegisterFontsForURL(odiaURL as CFURL,.process,&fontError) else {fatalError("Odia font registration failed")}
let odiaFont=CTFontCreateWithName("NotoSerifOriya-Regular" as CFString,21,nil)
guard CTFontCopyFamilyName(odiaFont) as String == "Noto Serif Oriya" else {fatalError("Odia font unexpectedly fell back")}


func registerDisplay(_ file:String)->String {
 let url=sourceRoot.appendingPathComponent("site/assets/fonts/"+file)
 guard CTFontManagerRegisterFontsForURL(url as CFURL,.process,nil),let descriptors=CTFontManagerCreateFontDescriptorsFromURL(url as CFURL) as? [CTFontDescriptor],let descriptor=descriptors.first else {fatalError("Display font registration failed")}
 return CTFontCopyPostScriptName(CTFontCreateWithFontDescriptor(descriptor,34,nil)) as String
}
let displayName=registerDisplay("CormorantGaramond-Variable.ttf")
let displayItalic=registerDisplay("CormorantGaramond-Italic-Variable.ttf")

var media = CGRect(x:0,y:0,width:595.28,height:841.89)
let consumer = CGDataConsumer(url:URL(fileURLWithPath:dest) as CFURL)!
let c = CGContext(consumer:consumer,mediaBox:&media,nil)!
let H=media.height
func color(_ hex:String)->CGColor { let n=UInt32(hex,radix:16)!;return CGColor(red:CGFloat((n>>16)&255)/255,green:CGFloat((n>>8)&255)/255,blue:CGFloat(n&255)/255,alpha:1) }
let ink=color("263C3C"), rust=color("963F28"), muted=color("655F51"), paper=color("F5EFDF"), rule=color("D2C6AC")
func fill(_ x:CGFloat,_ top:CGFloat,_ w:CGFloat,_ h:CGFloat,_ col:CGColor){c.setFillColor(col);c.fill(CGRect(x:x,y:H-top-h,width:w,height:h))}
func text(_ s:String,_ x:CGFloat,_ top:CGFloat,_ size:CGFloat,_ font:String="Helvetica",_ col:CGColor?=nil){var f=CTFontCreateWithName(font as CFString,size,nil);if font==displayName || font==displayItalic { f=CTFontCreateWithFontDescriptor(CTFontDescriptorCreateCopyWithVariation(CTFontCopyFontDescriptor(f),NSNumber(value:0x77676874),500),size,nil) };let a=NSAttributedString(string:s,attributes:[NSAttributedString.Key(kCTFontAttributeName as String):f,NSAttributedString.Key(kCTForegroundColorAttributeName as String):col ?? ink]);let line=CTLineCreateWithAttributedString(a);c.textPosition=CGPoint(x:x,y:H-top-CTFontGetAscent(f));CTLineDraw(line,c)}
func para(_ s:String,_ x:CGFloat,_ top:CGFloat,_ w:CGFloat,_ h:CGFloat,_ size:CGFloat=10.3){let f=CTFontCreateWithName("Helvetica" as CFString,size,nil);let ps=NSMutableParagraphStyle();ps.lineSpacing=3;let a=NSAttributedString(string:s,attributes:[NSAttributedString.Key(kCTFontAttributeName as String):f,NSAttributedString.Key(kCTForegroundColorAttributeName as String):ink,.paragraphStyle:ps]);let fs=CTFramesetterCreateWithAttributedString(a);let path=CGPath(rect:CGRect(x:x,y:H-top-h,width:w,height:h),transform:nil);let frame=CTFramesetterCreateFrame(fs,CFRange(location:0,length:0),path,nil);let visible=CTFrameGetVisibleStringRange(frame);if visible.length < a.length{fatalError("Text overflow: \(s)")};CTFrameDraw(frame,c)}
func section(_ n:String,_ title:String,_ body:String,_ x:CGFloat,_ top:CGFloat){fill(x,top,249,1,rule);text(n+"  "+title,x,top+12,12,"Helvetica-Bold",rust);para(body,x,top+35,249,75)}
c.beginPDFPage(nil);fill(0,0,595.28,841.89,paper)
text("EDITOR'S BRANDING CHEAT SHEET",34,27,10,"Helvetica-Bold",rust)
text("Kabita Live",34,52,34,displayName)

text("ମାଟିର ମହକ · ମନର ସ୍ୱର",34,118,21,"NotoSerifOriya-Regular",rust)
text("Poetry is an echo, asking a shadow to dance.",34,159,13,displayItalic)
text("English masthead. Odia signature. Three languages, with equal care.",34,184,9.6,"Helvetica",muted)
section("01","NAME & LANGUAGES","Use Kabita Live alone in the masthead. Keep the Odia signature separate. Put Odia, Hindi and English filters beside the poem lists, outside the header. Preserve each poem’s original script.",34,212)
section("02","PAPER & PAGE RHYTHM","Cotton paper: 16%. Poem pages: stable, varied monsoon or earth wash at 18%; soften on phones. Inner banners: 60% text, 40% art. Footer: ownership left, links right; both rows left-aligned on phones. No repeated signature. Keep night reading untextured.",311,212)
section("03","MAKE EACH COVER DISTINCT","Use a realistic artistic photograph or painterly-realistic image with one strong idea. Typeset the masthead separately. Keep issue/date and the signature legible. Record artist, rights and any AI use. Preserve historical originals.",34,336)
section("04","GIVE EACH WRITER A HOME","Preferred name and native script; approved portrait and biography; all contributions grouped by year/issue. Link every byline to the writer. Never invent a biography, publication count or social account.",311,336)
section("05","TYPE & COLOUR","Cormorant Garamond 500: English titles. Source Serif 4: reading. Noto Serif Oriya: Odia; Tiro Devanagari Hindi 400: Hindi. Character in titles, comfort in reading. Menu 17 px; poems 24/22 px. Preserve line breaks and natural script spacing.",34,460)
section("06","SHARE WITH THE CREDIT","Every shared piece keeps its full title, writer and original link. Link card: 1200 x 630. Square: 1080 x 1080. Story: 1080 x 1920, separately composed. Use excerpts only when approved. Never claim a post was sent.",311,460)
let swatches:[(String,String)] = [("Paper","F5EFDF"),("Ink","263C3C"),("Sea blue","125465"),("Laterite","963F28"),("Muted","655F51"),("Hearth","78643A")]
for (i,s) in swatches.enumerated(){let x=34+CGFloat(i)*89;fill(x,589,79,27,color(s.1));c.setStrokeColor(rule);c.stroke(CGRect(x:x,y:H-589-27,width:79,height:27));text(s.0,x,623,8.6,"Helvetica-Bold");text("#"+s.1,x,636,8.4,"Helvetica",muted)}
fill(34,669,527,1,rule)
text("BEFORE EACH ISSUE GOES LIVE",34,682,11,"Helvetica-Bold",rust)
para("Check: English name + Odia signature; all three languages; original verse + bylines; working writer and issue links; unique credited cover; readable mobile layout; correct sharing preview; complete archive records.",34,704,527,44,10.5)
text("Same masthead. A fresh cover. The poet's voice intact.",34,767,15,"Georgia")
text("Working editorial standard | 29 September 2026 | Companion: the visual branding guide",34,808,8,"Helvetica",muted)
c.endPDFPage();c.closePDF();print(dest)
