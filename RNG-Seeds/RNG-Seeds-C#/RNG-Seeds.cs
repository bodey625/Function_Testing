// See https://aka.ms/new-console-template for more information

using Microsoft.VisualBasic;

Console.WriteLine("\nHello, World! and welcome to this extremely basic example program");
Console.WriteLine("the purpose of this is to demonstrate RNG seed generation, loading " + 
      "specific RNG seeds, and incrementing RNG seeds. \n");

string seedString = "AHHHHH";
Random rng = new Random(seedString.GetHashCode());
/*  okay, we COULD use System.Security.Cryptography.RandomNumberGenerator.Create()
    to maintain secure random number generation, buta again, ENTIRELY unnecessary
    for a simple game seed generator. this may be a good site if youd like to learn more though:
    https://cryptobook.nakov.com/secure-random-generators/secure-random-generators-csprng
*/ 

Console.WriteLine("The current RNG Seed is   " + seedString);
Console.Write(rng.Next(1000) + "   ");


