using System.Security.Cryptography.X509Certificates;

//The following are autocreated to avoid warnings, I find those warnings very annoying ,-,
#pragma warning disable CS8602 // Desreferencia de una referencia posiblemente NULL.
#pragma warning disable CS8604 // Posible argumento de referencia nulo

internal class MyFirstProgram
{
    public MyFirstProgram(){}

    private static void Main(string[] args)
    {
     MyFirstProgram myFirstProgram = new MyFirstProgram();

        //FOLLOWING CODE IS FOR TESTING EXAMPLES
        Console.WriteLine(myFirstProgram.TrianglePerimeter(3,5));
        Console.WriteLine(myFirstProgram.ConcatenateStrings("Hello ", "World"));
        myFirstProgram.UserYearAndAge();
        Console.WriteLine(myFirstProgram.ListSum(new List<float>(){1,2,3,4,5,6,7,8,9,10,0}));
        Console.WriteLine(myFirstProgram.LargestString(new List<string>(){"hello","world", "taranguamicarotenericuaro", "lol", "1000003"}));
        myFirstProgram.AskForLicense();
        Console.WriteLine(myFirstProgram.FindKeyChar("Boo is not a boolean", 'o'));
        Console.WriteLine(myFirstProgram.IsPalindrome("Hannah"));
    }

    //PROBLEM #1
    //THIS METHOD INTAKES THE HEIGHT AND WIDTH OF A RIGHT TRIANGLE AND RETURNS THE PERIMETER.
    public float TrianglePerimeter(float width, float heigth){
        return MathF.Sqrt(width * width + heigth * heigth) + width + heigth;
    }

    //PROBLEM #2
    //INTAKES TWO STRINGS AND RETURNS A CONCATENATION OF THOSE TWO WORDS.
    public string ConcatenateStrings(string firstPart, string secondPart){
        return firstPart + secondPart;
    }

    //PROBLEM #3
    //THIS METHOD TAKES INPUT FROM THE USER TO DISPLAY IT WITH SOME TEXT.
    public void UserYearAndAge(){
        bool validUserName = false;
        bool validAge = false;
        string userName = "";
        string validChars = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ";
        string validNumbers = "0123456789";
        string userAge = "";

        //Loops until it gets a valid answer from user.
        while (!validUserName){
            Console.Write("Please enter your name: ");
            userName = Console.ReadLine();
            foreach (char s in userName.ToUpper()){
                validUserName = IsValidChar(s, validChars);

                if (!validUserName){
                Console.WriteLine("Your input might contain special characters such as (@!?- _) or spaces.");
                Console.WriteLine("Please try again using English/Spanish alphabet letters only.");
                break;
                }
            }
        }

        //Loops until it gets a valid answer from user.
        while (!validAge){
            Console.Write($"{userName} please enter your age (in whole years): ");
            userAge = Console.ReadLine();
            foreach (char s in userAge){
                validAge = IsValidChar(s, validNumbers);
                if (!validAge){
                Console.WriteLine("Your input might contain characters other than numeric.");
                Console.WriteLine("Please try again using only numeric characters.");
                break;
                }
            }
        }

        string year = "years";

        if (userAge == "1"){year = "year";}

        Console.WriteLine($"Your name is {userName} and you are {userAge} {year} old");
    }

    //PROBLEM #4
    //INTAKES A LIST OF FLOAT VALUES AND RETURNS THE SUM OF IT.
    public float ListSum(List<float> list)
    {
        float sum = 0;
        foreach (float value in list){
            sum += value;
        }
        return sum;
    }

    //PROBLEM #5
    /*INTAKES A LIST OF STRINGS AND RETURNS THE LONGEST AND IF 
    THERE ARE TWO OR MORE LONGEST IT RETURNS THE FIRST ONE IN THE LIST. */
    public string LargestString(List<string> list){
        string longest = "";
        foreach (string value in list){
            if(value.Length > longest.Length){ longest = value; }
        }

        return longest;
    }

    //PROBLEM #6
    //INTAKES A LICENSE NUMBER FROM THE USER AND RETURNS IF ITS VALID.
    public void AskForLicense(){

        bool isValid = false;

        //Loops until it gets a valid answer from user.
        while(!isValid){
            Console.Write("Please enter your license number: ");
            string licenseNum = Console.ReadLine();

            if(licenseNum != null){
                isValid = IsValidLicense(licenseNum.ToUpper());
            }
            if(isValid){
                Console.WriteLine("Your license number has been processed and it's valid!");
                break;
            }
            else{
                Console.WriteLine("Your license number it's not valid or no input was received");
                Console.WriteLine("Please Try Again!");
            }
        }
    }

    //INTAKES A STRING AND RETURNS WHETHER IT'S VALID BASED ON CERTIAN REQUIREMENTS.
    public bool IsValidLicense(string license){
        string validLetter = "ABCDEFGHIKLMNÑOPQRSTUVWXYZ";
        string validNum = "0123456789";
        bool hasNumber = false;

        //Requirements that are easier to check go first to optimize calculations.
        if(license == null){return false;}      
        if(!IsValidChar(license[0], validLetter)){return false;}
        if(!IsValidChar(license[license.Length-1], validLetter)){return false;}

        for(int i = 0; i < license.Length; i++){
            if(IsValidChar(license[i], validNum)){ 
                hasNumber = true; 
                break;
            }
        }

        if(!hasNumber){return false;}

        for(int i = 0; i < license.Length; i++){if(!IsValidChar(license[i], validLetter + validNum)){return false;}}

        return true;
    }

    //INTAKES A CHAR AND A STRING AND RETURNS WHETHER THE CHAR IS IN THE STRING.
    public bool IsValidChar(char letter, string acceptable){
        
        for (int i = 0; i < acceptable.Length; i++) {
            if(letter == acceptable[i]) {return true;}
        }
        return false;
    }

    //PROBLEM #7
    //INTAKES A STRING AND CHAR AND RETURNS THE AMOUNT OF TIMES THE CHAR IS IN THE STRING.
    public int FindKeyChar(string word, char key){
        int count = 0;

        foreach (char letter in word){
            if(letter == key){count++;}
        }

        return count;
    }

    //PROBLEM #8
    //INTAKES A STRING AND RETURNS WHEHER IT'S A PALINDROME OR NOT.
    public bool IsPalindrome(string word){
        string reverse = "";

        for(int i = 0; i < word.Length; i++){
            reverse = reverse + word[i];
            
        }

        return reverse.ToUpper() == word.ToUpper();
    }
}