# Candidate profile language (CFG / DSL with textX)

The goal is to represent a validated candidate profile in a domain-specific language.
Only profiles that follow the grammar are accepted; invalid ones are rejected
with the line and column of the error. Implementation: textX (resume.tx).

## EBNF

Resume        = "candidate" , STRING , "{" , Contact , Experience , { Experience } ,
                { Education } , Skills , Results , "}" ;
Contact       = "contact" , "{" , "email" , ":" , Email ,
                [ "phone" , ":" , Phone ] , "}" ;
Experience    = "experience" , "{" , "years" , ":" , INT ,
                "description" , ":" , STRING , "}" ;
Education     = "education" , "{" , "degree" , ":" , STRING , "}" ;
Skills        = "skills" , "{" , Skill , { "," , Skill } , "}" ;
Results       = "results" , "{" , ProfileResult , { ProfileResult } , "}" ;
ProfileResult = "profile" , ProfileName , ":" , Status ;
ProfileName   = "FULL_STACK_DEVELOPER" | "MACHINE_LEARNING_ENGINEER"
              | "DEVOPS_ENGINEER" | "DATA_ENGINEER" ;
Status        = "ACCEPTED" | "REJECTED" ;

Lexical terminals (regular expressions):
Email  = /[\w\.]+@[\w]+(\.[\w]+)+/ ;
Phone  = /\+?[0-9][0-9 \-]{6,14}[0-9]/ ;
Skill  = /[A-Z][A-Z0-9_]*/ ;
STRING = text between double quotes (textX built-in) ;
INT    = one or more digits (textX built-in) ;

## Non-terminals
Resume (start symbol), Contact, Experience, Education, Skills, Results,
ProfileResult, ProfileName, Status.

## Terminals
- Keywords: candidate, contact, email, phone, experience, years, description,
  education, degree, skills, results, profile.
- Punctuation: { } : ,
- Closed values: FULL_STACK_DEVELOPER, MACHINE_LEARNING_ENGINEER,
  DEVOPS_ENGINEER, DATA_ENGINEER, ACCEPTED, REJECTED.
- Lexical terminals: Email, Phone, Skill, STRING, INT.

## The grammar as a CFG G = (V, Σ, S, P)

V = the non-terminals above, Σ = the terminals above, S = Resume.
EBNF repetition is a shorthand for recursive productions. For example
Experience , { Experience } is equivalent to:

ExpList → Experience ExpList | Experience

and Skill , { "," , Skill } is equivalent to:

SkillList → Skill "," SkillList | Skill

All productions have a single non-terminal on the left side, so the grammar
is context-free (CyED III, slides 12-13).

## Structural characteristics
- Hierarchical (nested) structure: a Resume contains blocks, and each block
  contains fields between braces.
- Fixed order of blocks: contact, experience, education, skills, results.
- Repetition: one or more experiences, zero or more education entries, one or
  more skills (comma-separated), one or more profile results.
- Optional elements: phone.
- Closed alternatives: profile names and status only accept listed values.
- Lexical validation: emails, phones and skills must match their regular
  expressions (e.g. skills must be canonical symbols in uppercase).

## Example of a valid profile
```text
candidate "Tony Stark" {
  contact {
    email: tony.stark@avengers.com
    phone: +1 555 019 8273
  }
  experience {
    years: 15
    description: "Lead Engineer and AI Developer"
  }
  education {
    degree: "PhD Engineering"
  }
  skills {
    PYTHON, BASH, DOCKER, GIT
  }
  results {
    profile DEVOPS_ENGINEER: ACCEPTED
  }
}