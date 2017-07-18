<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
  xmlns:a="http://www.akomantoso.org/2.0"
  exclude-result-prefixes="a">

  <xsl:output method="html" />

  <xsl:template match="a:act">
    <xsl:element name="article" namespace="">
      <xsl:attribute name="class">akn-act</xsl:attribute>
      <xsl:apply-templates select="@*" />
      <xsl:apply-templates select="a:coverPage" />
      <xsl:apply-templates select="a:preface" />
      <xsl:apply-templates select="a:preamble" />
      <xsl:apply-templates select="a:body" />
      <xsl:apply-templates select="a:conclusions" />
    </xsl:element>
  </xsl:template>

  <!-- copy over attributes using a data- prefix, except for 'id' which is copied as-is -->
  <xsl:template match="@*" >
    <xsl:choose>
      <xsl:when test="local-name(.) = 'id'">
        <xsl:attribute name="{local-name(.)}">
          <xsl:value-of select="." />
        </xsl:attribute>
      </xsl:when>
      <xsl:otherwise>
        <xsl:variable name="attName" select="concat('data-', local-name(.))"/>
        <xsl:attribute name="{$attName}">
          <xsl:value-of select="." />
        </xsl:attribute>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <!-- for parts and chapters, include an easily stylable heading -->
  <xsl:template match="a:part">
    <section class="akn-part">
      <xsl:apply-templates select="@*" />
      <h2>
        <xsl:text>Part </xsl:text>
        <xsl:value-of select="./a:num" />
        <xsl:text> - </xsl:text>
        <xsl:value-of select="./a:heading" />
      </h2>
      
      <xsl:apply-templates select="./*[not(self::a:num) and not(self::a:heading)]" />
    </section>
  </xsl:template>

  <xsl:template match="a:chapter">
    <section class="akn-chapter">
      <xsl:apply-templates select="@*" />
      <h2>
        
        
        <span class="num">
          <xsl:choose>
            <xsl:when test="./a:num[@explainurl]">
              <xsl:element name="a">
                <xsl:attribute name="href">
                  <xsl:value-of select="./a:num/@explainurl"/>
                </xsl:attribute>
                
                <xsl:text>Chapter </xsl:text>
                <xsl:value-of select="./a:num" />
                
                <xsl:text> </xsl:text>
                <xsl:value-of select="./a:heading" />
                
              </xsl:element>
            </xsl:when>
            <xsl:otherwise>
              
              <xsl:text>Chapter </xsl:text>
              <xsl:value-of select="./a:num" />
              
              <xsl:text> </xsl:text>
              <xsl:value-of select="./a:heading" />
              
            </xsl:otherwise>
          </xsl:choose>
        </span>
        
      </h2>
      
      <xsl:apply-templates select="./*[not(self::a:num) and not(self::a:heading)]" />
    </section>
  </xsl:template>

  <xsl:template match="a:section">
    <section class="akn-section ui grid ">
      <div class="sixteen wide column ">
        <xsl:apply-templates select="@*" />
        <h3>
          <span class="num">
            <xsl:choose>
              <xsl:when test="./a:num[@explainurl]">
                <xsl:element name="a">
                  <xsl:attribute name="href">
                    <xsl:value-of select="./a:num/@explainurl"/>
                  </xsl:attribute>
                  <xsl:value-of select="./a:num" />
                </xsl:element>
              </xsl:when>
              <xsl:otherwise>
                <xsl:value-of select="./a:num" />
              </xsl:otherwise>
            </xsl:choose>
          </span>
          <xsl:text> </xsl:text>
          <xsl:value-of select="./a:heading" />
        </h3>
      
        <xsl:apply-templates select="./*[not(self::a:num) and not(self::a:heading) and not(self::a:explain)]" />
      
      </div>
    </section>
  </xsl:template>

  <!-- components/schedules -->
  <xsl:template match="a:doc">
    <article class="akn-doc">
      <xsl:apply-templates select="@*" />
      <xsl:if test="a:meta/a:identification/a:FRBRWork/a:FRBRalias">
        <h2>
          <xsl:value-of select="a:meta/a:identification/a:FRBRWork/a:FRBRalias/@value" />
        </h2>
      </xsl:if>

      <xsl:apply-templates select="a:coverPage" />
      <xsl:apply-templates select="a:preface" />
      <xsl:apply-templates select="a:preamble" />
      <xsl:apply-templates select="a:mainBody" />
      <xsl:apply-templates select="a:conclusions" />
    </article>
  </xsl:template>

  <!-- for block elements, generate a span element with a class matching
       the AN name of the node and copy over the attributes -->
  <xsl:template match="a:coverPage | a:preface | a:preamble | a:conclusions">
    <section class="akn-{local-name()}">
      <xsl:apply-templates select="@*" />
      <xsl:apply-templates />
    </section>
  </xsl:template>

  <!-- for all nodes, generate a SPAN element with a class matching
       the AN name of the node and copy over the attributes -->
  <xsl:template match="*">
    <span class="akn-{local-name()}">
      <xsl:apply-templates select="@*" />
      <xsl:apply-templates />
    </span>
  </xsl:template>
  
  <!-- For HTML table elements, copy them over then apply normal AN
       processing to their contents -->
  <xsl:template match="a:table ">
    <div style="overflow-x:auto;">
    <xsl:element name="{local-name()}">
      <xsl:copy-of select="@*" />
      <xsl:apply-templates />
    </xsl:element>
  </div>
  </xsl:template>
  
  <!-- For HTML table elements, copy them over then apply normal AN
       processing to their contents -->
  <xsl:template match="a:tr | a:th | a:td">
    <xsl:element name="{local-name()}">
      <xsl:copy-of select="@*" />
      <xsl:apply-templates />
    </xsl:element>
  </xsl:template>

  <!-- special HTML elements -->
  <xsl:template match="a:a | a:abbr | a:b | a:i | a:span | a:sub | a:sup | a:u | a:ul | a:li">
    <xsl:element name="{local-name()}">
      <xsl:copy-of select="@*" />
      <xsl:apply-templates />
    </xsl:element>
  </xsl:template>
  
  <xsl:template match="a:strong ">
    <b>
      <xsl:element name="{local-name()}">
        <xsl:copy-of select="@*" />
        <xsl:apply-templates />
      </xsl:element>
    </b>
  </xsl:template>
  
  <xsl:template match="a:em ">
    <i>
      <xsl:element name="{local-name()}">
        <xsl:copy-of select="@*" />
        <xsl:apply-templates />
      </xsl:element>
    </i>
  </xsl:template>
  
  <xsl:template match="a:enewline ">
    <p>
      <xsl:text> </xsl:text> 
    </p>
  </xsl:template>
  
  <xsl:template match="a:br ">
    <p>
      <xsl:text> </xsl:text> 
    </p>
  </xsl:template>
  
  <xsl:template match=" a:h1 | a:h2 | a:h3 | a:h4 ">
      <xsl:element name="{local-name()}">
        <xsl:copy-of select="@*" />
        <xsl:apply-templates />
      </xsl:element>
  </xsl:template>
  

</xsl:stylesheet>