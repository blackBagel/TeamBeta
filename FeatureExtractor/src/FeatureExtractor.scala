import java.nio.charset.CodingErrorAction

import scala.collection.parallel.ParMap
import scala.collection.parallel.mutable.ParArray
import java.io.{BufferedWriter, OutputStreamWriter, FileOutputStream, File}
import scala.io.Source.fromFile
import scala.io.Codec
import scala.util.matching.Regex

/**
  * Created by Jbt on 11/9/2015.
  */
object FeatureExtractor {
  def main(args:Array[String]) = {

    val asmFolder = """C:\Users\Jbt\Desktop\temp"""
    val importedFunctionNameRegex = """extrn (\S*)""".r
    val importedDllRegex = """; Imports from ([a-zA-Z0-9]*.dll)""".r
    val outputFolderPath = """C:\Users\Jbt\Desktop\temp\out"""

    val matches = findAllMatchesForMultipleFeatures(asmFolder,Array(importedDllRegex,importedFunctionNameRegex))
    outputMultipleFeaturesMatches(matches,outputFolderPath)

    println("Break")

  }

  private def findAllMatches(asmFolderPath: String, regex: Regex): ParMap[String,List[String]] = {
    implicit val codec = Codec("UTF-8")

    codec.onMalformedInput(CodingErrorAction.IGNORE)
    codec.onUnmappableCharacter(CodingErrorAction.IGNORE)

    val asmFiles = ParArray() ++ new File(asmFolderPath).listFiles.filter(_.isFile).filter(_.getName.endsWith(".asm"))
    val asmFilesContents = asmFiles map(file => (file.getName(),fromFile(file).mkString)) toMap

    asmFilesContents mapValues(regex findAllMatchIn ) mapValues(_ map(_ group(1))) mapValues(_ toList)
  }

  private def findAllMatchesForMultipleFeatures(asmFolderPath: String, regexs: Array[Regex]): ParMap[String,List[List[String]]] = {
    implicit val codec = Codec("UTF-8")

    codec.onMalformedInput(CodingErrorAction.IGNORE)
    codec.onUnmappableCharacter(CodingErrorAction.IGNORE)

    val asmFiles = ParArray() ++ new File(asmFolderPath).listFiles.filter(_.isFile).filter(_.getName.endsWith(".asm"))
    val asmFilesContents = asmFiles map(file => (file.getName(),fromFile(file).mkString)) toMap

    regexs map (regex =>  asmFilesContents mapValues(regex findAllMatchIn ) mapValues(_ map(_ group(1))) mapValues(_ toList) ) map(_ mapValues(l => List(l))) reduce((m1,m2) => {
      m1 ++ m2.map { case (k,v) => k -> (v ++ m1.getOrElse(k,List())) }} )

  }

  private def outputMatches(matches:ParMap[String,List[String]], outputFolderPath: String) = {
    matches foreach{ case (fileName,matches) => {
      val writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(outputFolderPath + "\\"+ fileName +".csv"))))
      for ( line <- matches) {
        writer.write(line + "\n")
      }
      writer.close()

    }}
  }

  private def outputMultipleFeaturesMatches(multipleFeaturesMatches:ParMap[String,List[List[String]]], outputFolderPath: String) = {
    multipleFeaturesMatches foreach{ case (fileName,matches) => {
      val writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(outputFolderPath + "\\"+ fileName +".csv"))))
      for ( m <- matches) {
        for(featureValue <- m)
          writer.write(featureValue + "\n")
        writer.write(",")
      }
      writer.close()

    }}
  }

  }
