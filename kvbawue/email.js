//This is a first layer of deobfuscation.
						    //Basically a reversed ROT13 algorithm.
						    function changeLetters(string) {

						        //Helper variables.
						        var currentLetter,
						            currentPos,
						            currentString = "",

						            //Behold! The one and only counter.
						            i = 0,

						            //We"re going to loop through the obfuscated strings characters, so this will come in handy.
						            stringLength = string.length - 1,

						            //Characters that will be used when deobfuscating email address.
						            //Same as string in PHP obfuscate function (obfuscateEmail).
						            characters = "123456789qwertzuiopasdfghjklyxcvbnmMNBVCXYLKJHGFDSAPOIUZTREWQ",
						            charactersLength = characters.length;


						        //Counter variable has been declared before.
						        for( ; i<stringLength; i++ ) {

						            //This letter will be deobfuscated.
						            currentLetter = string.charAt(i);

						            //Position of the letter in our characters string.
						            currentPos = characters.indexOf(currentLetter);

						            //If character is present in our string, replace it with a character
						            //30 places before (opposite from obfuscating).
						            //If not, leave it as it is (because character wasn"t obfuscated).
						            if( currentPos > -1 ) {

						                currentPos -= (charactersLength-1) / 2;
						                currentPos = currentPos < 0 ? charactersLength + currentPos : currentPos;

						            } else {

						                currentString += currentLetter;

						            }

						            //Finally, append a character to our temp string that will be returned.
						            currentString += characters.charAt(currentPos);

						        }

						        return currentString;

						    }

						    //Function that will handle email deobfuscation.
						    //@param element is a reference to html element that will be deobfuscated.
						    //Deobfuscation is done on text and on href attribute of the element.
						    //Nevertheless, function will work well with any element you pass in,
						    //even if href attribute won"t be present.
						    function deObfuscateEmail( element ) {

						        //Get the text of the element.
						        var text = element.innerHTML,

						            //Get href attribute. If there is no href attribute, set href value to be an empty string.
						            //Regular expression is an IE Fix.
						            //Namely, IE appends obfuscated email to the url (www.domain.com/com.liameym@em).
						            //Therefore, the first part of the link needs to be removed (we grab just everything after the last forward slash "/").
						            href = element.getAttribute("href").replace(/http:\/\/(.+)\//gi, "") || "",

						            //Control variable. if the two @ symbols are present, we will perform deobfuscation,
						            //if not, the string is not obfuscated and doesn"t have to be deobfuscated.
						            textReplace = text.search(/@.+@/),
						            hrefReplace = href.search(/@.+@/),

						            //This function handles the second layer of deobfuscation.
						            //It is called later in the code.
						            //Letters of the email are reversed (again) and css direction returned back to ltr.
						            //This is called on mouseover event.
						            reverseEmails = function(){

						                //Only if htef is obfuscated.
						                if( hrefReplace > -1 ) {

						                    //That"s the reversing part right here.
						                    element.setAttribute("href", href.split("").reverse().join("") );

						                }

						                //Only if text is obfuscated.
						                if( textReplace > -1 ) {

						                    //Reverse the text of the element and
						                    //return the direction to normal (left to right).
						                    element.innerHTML = text.split("").reverse().join("");
						                    element.style.direction = "ltr";
						                    element.style.unicodeBidi = "normal";

						                }


						                //Letters are replaced and the event isn"t needed anymore.
						                if( element.removeEventListener ) {

						                    element.removeEventListener("mouseover", reverseEmails, false);

						                } else {

						                    // IE8-
						                    element.detachEvent("onmouseover", reverseEmails);

						                }


						            };
						            //End variables and functions definitions.


						        //href has to be processed first, because of the strange
						        //IE bug that will mix the href and innerHTML values.
						        if( hrefReplace > -1 ) {

						            href = changeLetters(href);
						            element.setAttribute("href", href);

						        }

						        //Change the direction of the text to show real address
						        //to users, instead of a reversed one.
						        if( textReplace > -1 ) {

						            text = changeLetters( text );
						            element.innerHTML = text;
						            element.style.direction = "rtl";
						            element.style.unicodeBidi = "bidi-override";
									element.style.whiteSpace = "nowrap";
						        }


						        //Since we have a rtl text, user can"t copy or click on a link.
						        //Therefore we"ll replace the value as soon as user hovers over the link.
						        if( element.addEventListener ) {

						            element.addEventListener("mouseover", reverseEmails, false);

						        } else {

						            element.attachEvent("onmouseover", reverseEmails);

						        }

						    }



						    //We could use native getElementsByClassName in browsers that support this method,
						    //but I did a few quick tests and it seems to be slower.
						    //If you have more info on performance getElementsByClassName vs getElementsByTagName + className.indexOf please let me know.
						    //var obfuscatedEmails = document.getElementsByClassName("obfuscatedEmail"),

						    //This is written to be as general as possible; you can leave this part out and just call
						    //deObfuscateEmail() manually on elements that should be deobfuscated.

						    var obfuscatedEmails = document.getElementsByTagName("a"),
						        obfuscatedEmailsLength = obfuscatedEmails.length,
						        i = 0;

						    for( ; i<obfuscatedEmailsLength; i++ ) {

						        if( obfuscatedEmails[i].className.indexOf("obfuscatedEmail") > -1 ) {

						            deObfuscateEmail( obfuscatedEmails[i] );

						        }

						    }
