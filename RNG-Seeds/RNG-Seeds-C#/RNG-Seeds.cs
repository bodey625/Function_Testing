// See https://aka.ms/new-console-template for more information




Console.WriteLine("\nHello, World! and welcome to this extremely basic example program");
Console.WriteLine("the purpose of this is to demonstrate RNG seed generation, loading " + 
"specific RNG seeds, and incrementing RNG seeds. \n");


var seedString = DateTime.UtcNow.ToString("ddMfffffff"); // THIS STRING HAS TO BE AN INT VALUE
// hmmmmm. int32 might not be big enough for reliably random games. 10 digits is pretty small
Random rng = new Random(int.Parse(seedString));


while (true) {

    /*  Seems like we wont be able to easily convert a string into an int for the seed here,
        i could of course still manage it manually by converting each letter in the string
        into its UTF-8 value, but thats a very specific need for a relatively unimportant feature
    */
    Console.WriteLine("The current RNG Seed is   " + seedString);
    Console.WriteLine("enter 0 to exit program | 1 to enter a new seed | 2 to increment seed('2 x' will print x values)");

    var readline = Console.ReadLine();

    if (readline == "0") { // Exit the program
        break;
    }
    else if (readline == "1") { // Change the rng seed
        Console.WriteLine("Enter seed, or leave blank for same seed");
        readline = Console.ReadLine();

        try { // have to check the new seed for letters
            // check if readline has anything in it
            if (readline == null) { Console.WriteLine("seedString was not changed");
            } else { seedString = readline; }

            rng = new Random(int.Parse(seedString)); // update rng with new seedString
            /*  okay, we COULD use System.Security.Cryptography.RandomNumberGenerator.Create()
                to maintain secure random number generation, buta again, ENTIRELY unnecessary
                for a simple game seed generator. this may be a good site if youd like to learn more though:
                https://cryptobook.nakov.com/secure-random-generators/secure-random-generators-csprng
            */ 
            
        } catch (FormatException){  // catch any letters that would force seedString to remain a string
            Console.WriteLine("Oi. sorry mate, this one only accepts integer seeds.");
        }
    } 
    else if (readline == "2") { // print off next rng numbers
        for(int i = 0; i < 5; i++)
            Console.Write(" {0} ", rng.Next(1000));
        Console.WriteLine();
    }

}

