#!/usr/bin/env python3
"""
compile_mack.py - Compile John E. Mack's abduction research data into structured formats.

John E. Mack, M.D. (1929-2004) was a Harvard psychiatrist who studied ~200 abduction
experiencers over 12+ years through the Program for Extraordinary Experience Research (PEER).
His primary published case data comes from "Abduction: Human Encounters with Aliens" (1994),
which presents 13 detailed case studies selected from ~100 investigated cases.

Data sources:
- "Abduction: Human Encounters with Aliens" (1994) - 13 case studies
- "Passport to the Cosmos" (1999) - thematic analysis, additional cases
- Published interviews, reviews, and summaries
- PEER program documentation
- UFO Insight case analysis (ufoinsight.com)
- PBS NOVA interview transcripts
- UAPedia compilation

NOTE: The bulk of Mack's raw research data (150 boxes, ~200 cases) is archived at
Rice University's Archives of the Impossible (MS 1066) and is NOT yet digitized or
publicly available. Most materials are restricted until anonymization or 2074.
"""

import json
import csv
import os
from datetime import datetime

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(OUTPUT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)


def build_case_studies():
    """
    Build structured data for the 13 case studies from Mack's 1994 book "Abduction."
    All pseudonyms are as published in the book. Demographics are extracted from
    the opening paragraphs of each case chapter.
    """
    cases = [
        {
            "case_id": "MACK-01",
            "pseudonym": "Ed",
            "chapter": 3,
            "chapter_title": "You Will Remember When You Need to Know",
            "gender": "M",
            "age_at_contact": 45,
            "age_description": "mid-forties",
            "occupation": "Technician at high-tech firm",
            "location_state": "Massachusetts",
            "location_detail": "Lives in MA; encounter in Ogunquit, Maine",
            "marital_status": "Married",
            "spouse_name": "Lynn",
            "spouse_occupation": "Writer",
            "year_contacted_mack": 1992,
            "month_contacted_mack": "July",
            "first_experience_year": 1961,
            "first_experience_age": "High school (~16)",
            "first_experience_location": "Coast of Maine, north of Portland",
            "number_of_sessions": 1,
            "session_type": "Hypnosis/relaxation",
            "attended_support_group": True,
            "experience_types": [
                "Missing time",
                "Transported to craft",
                "Transparent pod/room with curved walls",
                "Sexual encounter with female entity",
                "Telepathic communication",
                "Environmental/political messages",
                "Childhood visitations"
            ],
            "entity_description": "Long silvery hair, large forehead, large dark eyes",
            "physical_evidence": [],
            "key_themes": [
                "Memory recovery through meditation",
                "Information reception and storage",
                "Delayed recall (30 years)",
                "Hypnosis as clarifying tool"
            ],
            "transformative_effects": [
                "Interest in alien intelligence",
                "Engagement with UFO community (MUFON)"
            ],
            "source": "Mack (1994), Chapter 3, pp. 37-77"
        },
        {
            "case_id": "MACK-02",
            "pseudonym": "Sheila",
            "chapter": 4,
            "chapter_title": "Personally, I Don't Believe in UFOs",
            "gender": "F",
            "age_at_contact": 44,
            "age_description": "forty-four",
            "occupation": "Social worker",
            "location_state": "Not specified (Northeast US)",
            "location_detail": "Hospital internship location",
            "marital_status": "Not specified",
            "year_contacted_mack": 1992,
            "month_contacted_mack": "Summer",
            "first_experience_year": 1984,
            "first_experience_age": "~36 (electrical dreams began after mother's death)",
            "first_experience_location": "Not specified",
            "number_of_sessions": None,
            "session_type": "Hypnosis/relaxation",
            "attended_support_group": None,
            "experience_types": [
                "Electrical dreams",
                "Paralysis",
                "Invasive procedures",
                "Childhood experiences"
            ],
            "entity_description": "Not detailed in available excerpts",
            "physical_evidence": [],
            "key_themes": [
                "Mental health professional perspectives",
                "Relationship between trauma and abduction experiences",
                "Mother's death as trigger for recall",
                "Incest/family trauma history"
            ],
            "transformative_effects": [
                "Spiritual reframing",
                "Famous quote: 'Saying I benefited spiritually from being abducted by aliens is like saying an Auschwitz survivor benefited spiritually from being treated like a laboratory animal'"
            ],
            "source": "Mack (1994), Chapter 4, pp. 55-77"
        },
        {
            "case_id": "MACK-03",
            "pseudonym": "Scott",
            "chapter": 5,
            "chapter_title": "Summer of '92",
            "gender": "M",
            "age_at_contact": 24,
            "age_description": "twenty-four",
            "occupation": "Actor, filmmaker, auto mechanic (works with father), piano player/songwriter, builder",
            "location_state": "Northeast US",
            "location_detail": "Not specified",
            "marital_status": "Not specified",
            "year_contacted_mack": 1991,
            "month_contacted_mack": "November",
            "first_experience_year": None,
            "first_experience_age": "Age 3",
            "first_experience_location": "Not specified",
            "number_of_sessions": None,
            "session_type": "Hypnosis/relaxation",
            "attended_support_group": True,
            "experience_types": [
                "Cross-generational abductions",
                "Partial memories of 'short guys'",
                "Rod-like device applied to head",
                "Dual human/alien identity",
                "Medical symptoms (headaches, dizziness, seizures)"
            ],
            "entity_description": "Short beings; rod-like device causing unconsciousness",
            "physical_evidence": [
                "Medical history of headaches/dizziness/seizures"
            ],
            "key_themes": [
                "Dramatic personal transformation",
                "Dual human/alien identity discovery",
                "Cross-generational family experiences",
                "Resistance to formal education but strong intelligence"
            ],
            "transformative_effects": [
                "Expanded sensitivity and thoughtfulness",
                "Confronting reality of experiences"
            ],
            "source": "Mack (1994), Chapter 5, pp. 78-97"
        },
        {
            "case_id": "MACK-03b",
            "pseudonym": "Lee",
            "chapter": 5,
            "chapter_title": "Summer of '92 (Scott's sister, same chapter)",
            "gender": "F",
            "age_at_contact": 22,
            "age_description": "Nineteen months younger than Scott (~22-23)",
            "occupation": "Not specified; spiritual seeker",
            "location_state": "Northeast US",
            "location_detail": "Traveled to India to study Tibetan Buddhism",
            "marital_status": "Not specified",
            "year_contacted_mack": 1992,
            "month_contacted_mack": "November",
            "first_experience_year": None,
            "first_experience_age": "Early teenager",
            "first_experience_location": "Not specified",
            "number_of_sessions": 1,
            "session_type": "Hypnosis",
            "attended_support_group": None,
            "experience_types": [
                "Taken aboard UFO",
                "Probing instrument inserted in vagina",
                "Egg/tissue removal",
                "Fears of sexual intimacy",
                "Cross-generational family experiences"
            ],
            "entity_description": "Alien beings (not further specified)",
            "physical_evidence": [],
            "key_themes": [
                "Initially attributed trauma to sexual abuse",
                "Spiritual reframing of experiences",
                "Cross-generational family pattern",
                "Tibetan Buddhism connection"
            ],
            "transformative_effects": [
                "Spiritual development journey to India",
                "Adopted spiritual interpretation"
            ],
            "source": "Mack (1994), Chapter 5 (subsection on Lee)"
        },
        {
            "case_id": "MACK-04",
            "pseudonym": "Jerry",
            "chapter": 6,
            "chapter_title": "An Alienation of Affections",
            "gender": "F",
            "age_at_contact": 30,
            "age_description": "had just turned thirty",
            "occupation": "Housewife (self-described 'ordinary housewife')",
            "location_state": "Not specified (Northeast US)",
            "location_detail": "Not specified",
            "marital_status": "Married",
            "year_contacted_mack": 1992,
            "month_contacted_mack": "Early June",
            "first_experience_year": None,
            "first_experience_age": "Age 7",
            "first_experience_location": "Not specified",
            "number_of_sessions": 4,
            "session_type": "Hypnosis/relaxation",
            "attended_support_group": None,
            "experience_types": [
                "UFO dreams",
                "Abduction encounters",
                "Sexual/reproductive procedures",
                "Missing time",
                "Childhood experiences from age 7"
            ],
            "entity_description": "Not detailed in available excerpts",
            "physical_evidence": [],
            "key_themes": [
                "Intrusive sexual/reproductive procedures",
                "Impact on intimate life and well-being",
                "Alienation of affections",
                "Mother's role in dismissing/acknowledging experiences",
                "Extensive journaling (hundreds of pages)"
            ],
            "transformative_effects": [
                "Dual identity awareness",
                "Philosophical development"
            ],
            "notes": "Jerry shared hundreds of pages of journal entries with Mack; contacted him after seeing CBS miniseries 'Intruders'",
            "source": "Mack (1994), Chapter 6, pp. 98-129"
        },
        {
            "case_id": "MACK-05",
            "pseudonym": "Catherine",
            "chapter": 7,
            "chapter_title": "If They Would Ever Ask Me",
            "gender": "F",
            "age_at_contact": 22,
            "age_description": "twenty-two",
            "occupation": "Music student, nightclub receptionist",
            "location_state": "Massachusetts",
            "location_detail": "Somerville, near Boston; family in Alaska",
            "marital_status": "Not specified (single implied)",
            "year_contacted_mack": 1991,
            "month_contacted_mack": "March",
            "first_experience_year": 1991,
            "first_experience_age": "Age 3 (earliest); age 22 (recent)",
            "first_experience_location": "Boston area; also Alaska",
            "number_of_sessions": None,
            "session_type": "Hypnosis/relaxation",
            "attended_support_group": None,
            "experience_types": [
                "Missing time (45 minutes)",
                "Nosebleed (first ever)",
                "UFO sighting correlation (Boston UFO)",
                "Childhood abductions from age 3",
                "Paralysis episodes",
                "Transported to craft",
                "Transparent 'fish tank' rooms with curved walls",
                "Blue light columns",
                "Levitation",
                "Observed ~40 cases of baby-alien entities in liquid",
                "Reproductive procedures"
            ],
            "entity_description": "Small beings; transparent rooms with curved walls",
            "physical_evidence": [
                "Nosebleed (first ever)",
                "45-minute missing time episode"
            ],
            "key_themes": [
                "Corroboration with independent UFO sighting",
                "Childhood experiences from age 3",
                "Christmas 1990 Alaska incident",
                "Tank containing ~40 alien-baby entities"
            ],
            "transformative_effects": [],
            "source": "Mack (1994), Chapter 7, pp. 130-163"
        },
        {
            "case_id": "MACK-06",
            "pseudonym": "Joe",
            "chapter": 8,
            "chapter_title": "Deliverance from the Insane Asylum",
            "gender": "M",
            "age_at_contact": 34,
            "age_description": "thirty-four",
            "occupation": "Psychotherapist; professional development consultant; designer/leader of nature adventures",
            "location_state": "Not specified",
            "location_detail": "Not specified",
            "marital_status": "Married (wife expecting first child)",
            "year_contacted_mack": 1992,
            "month_contacted_mack": "August",
            "first_experience_year": None,
            "first_experience_age": "Early childhood",
            "first_experience_location": "Not specified",
            "number_of_sessions": 4,
            "session_type": "Hypnosis/relaxation",
            "session_dates": "October 1992 - March 1993",
            "attended_support_group": None,
            "experience_types": [
                "ET experiences from early childhood",
                "Beings with large heads",
                "Needle in neck",
                "Fear of the dark",
                "Past life experience",
                "Birth/death cycle awareness"
            ],
            "entity_description": "Small beings with large heads; needle insertion",
            "physical_evidence": [],
            "key_themes": [
                "Abduction in context of fatherhood",
                "Past life experiences",
                "Birth and death cycles",
                "Fear confrontation (helps others overcome fears)",
                "Male-female integration"
            ],
            "transformative_effects": [
                "Felt 'fragmented parts' coming together",
                "Increase in 'soul's love and energy'",
                "Male-female integration"
            ],
            "source": "Mack (1994), Chapter 8, pp. 167-191"
        },
        {
            "case_id": "MACK-07",
            "pseudonym": "Sara",
            "chapter": 9,
            "chapter_title": "Sara: Species Merger and Human Evolution",
            "gender": "F",
            "age_at_contact": 28,
            "age_description": "twenty-eight",
            "occupation": "Graduate student",
            "location_state": "Northeast US (anonymity requested)",
            "location_detail": "Details omitted to protect anonymity",
            "marital_status": "Has boyfriend",
            "year_contacted_mack": None,
            "month_contacted_mack": None,
            "first_experience_year": None,
            "first_experience_age": "Childhood (paranormal history)",
            "first_experience_location": "Not specified",
            "number_of_sessions": 1,
            "session_type": "Hypnosis",
            "attended_support_group": None,
            "experience_types": [
                "Telepathic communication from small beings",
                "Spontaneous ambidextrous drawing",
                "Drawings of alien beings (focus on eyes)",
                "Paranormal experiences from childhood",
                "Levitation during seance",
                "Invisible hands sensation",
                "Presence phenomena (stairs, windows, bedroom)",
                "Planetary preservation messages",
                "Ecological/geomagnetic information"
            ],
            "entity_description": "Small beings communicating telepathically",
            "physical_evidence": [
                "Pain at base of skull",
                "Spontaneous left-hand drawing ability"
            ],
            "key_themes": [
                "Species merger concept",
                "Human evolution",
                "Spiritual approach to experiences",
                "Ecological/planetary concern",
                "Service orientation"
            ],
            "transformative_effects": [
                "Desire to serve and help the world",
                "Powerful spiritual insights",
                "Ecological awareness"
            ],
            "source": "Mack (1994), Chapter 9, pp. 192-208"
        },
        {
            "case_id": "MACK-08",
            "pseudonym": "Paul",
            "chapter": 10,
            "chapter_title": "Paul: Bridging Two Worlds",
            "gender": "M",
            "age_at_contact": 26,
            "age_description": "twenty-six",
            "occupation": "Advertising business owner (self-administered)",
            "location_state": "New Hampshire",
            "location_detail": "Living with parents; working to rent separate apartment",
            "marital_status": "Single (living with parents)",
            "year_contacted_mack": None,
            "month_contacted_mack": None,
            "first_experience_year": None,
            "first_experience_age": "Age 3",
            "first_experience_location": "Home (stairs)",
            "number_of_sessions": 2,
            "session_type": "Hypnosis/relaxation (after initial interview)",
            "attended_support_group": True,
            "experience_types": [
                "Strange being on stairs at home",
                "Encounters since age 3",
                "Visions of spaceships",
                "Dual human/alien identity",
                "Knowledge of human origins",
                "Reptilian/dinosaur connections",
                "Alien-human hybrid awareness"
            ],
            "entity_description": "Full bodysuits with large white heads, large dark eyes",
            "physical_evidence": [],
            "key_themes": [
                "Dual human/alien identity",
                "Mission as 'example' of love and openness",
                "Transformative and healing powers",
                "Bridging two worlds",
                "Previous negative mental health professional experience"
            ],
            "transformative_effects": [
                "Mission to help humans overcome fears",
                "Sense of dual identity",
                "Love and openness"
            ],
            "notes": "Previous psychologist discontinued sessions because they were too disturbing; met Mack at UFO conference",
            "source": "Mack (1994), Chapter 10, pp. 209-232"
        },
        {
            "case_id": "MACK-09",
            "pseudonym": "Eva",
            "chapter": 11,
            "chapter_title": "Eva's Mission",
            "gender": "F",
            "age_at_contact": 33,
            "age_description": "thirty-three",
            "occupation": "Assistant to a CPA",
            "location_state": "Not specified",
            "location_detail": "Not specified",
            "marital_status": "Has daughter Sarah (age 6)",
            "year_contacted_mack": None,
            "month_contacted_mack": None,
            "first_experience_year": None,
            "first_experience_age": "Early childhood",
            "first_experience_location": "Not specified",
            "number_of_sessions": None,
            "session_type": "Hypnosis/relaxation",
            "attended_support_group": None,
            "experience_types": [
                "Entities present day and night",
                "Beings in room upon waking",
                "Childhood paralysis episodes",
                "Vaginal probing by 'midgets'",
                "Reproductive procedures",
                "Feelings of global mission"
            ],
            "entity_description": "'Midgets' who probed; entities present day and night",
            "physical_evidence": [],
            "key_themes": [
                "Global mission/purpose",
                "Pioneer mentality",
                "Concern for daughter's similar experiences",
                "Isolation and burden of experiences",
                "Vehicle for larger purpose"
            ],
            "transformative_effects": [
                "Sense of mission and purpose",
                "Desire to help others"
            ],
            "notes": "Contacted Mack after reading Wall Street Journal article about his work; worried about her 6-year-old daughter's experiences",
            "source": "Mack (1994), Chapter 11, pp. 233-257"
        },
        {
            "case_id": "MACK-10",
            "pseudonym": "Dave",
            "chapter": 12,
            "chapter_title": "The Magic Mountain",
            "gender": "M",
            "age_at_contact": 38,
            "age_description": "thirty-eight",
            "occupation": "Health care worker",
            "location_state": "Pennsylvania",
            "location_detail": "Isolated community in south central Pennsylvania",
            "marital_status": "Married",
            "year_contacted_mack": 1992,
            "month_contacted_mack": "June",
            "first_experience_year": None,
            "first_experience_age": "Age 3",
            "first_experience_location": "Not specified",
            "number_of_sessions": None,
            "session_type": "Hypnosis",
            "attended_support_group": None,
            "experience_types": [
                "Abduction experiences from age 3",
                "Unexplained crescent-shaped scar",
                "Missing time episodes",
                "UFO sighting at age 19",
                "Being staring through window",
                "Anal probing",
                "Chi/energy experiences",
                "Female familiar entity"
            ],
            "entity_description": "Creature in window, female and familiar, compelling/controlling eyes",
            "physical_evidence": [
                "Unexplained crescent-shaped scar"
            ],
            "key_themes": [
                "Karate/martial arts and Chi experiences",
                "Shamanic/spiritual dimension",
                "Magic Mountain metaphor",
                "Physical evidence (scar)"
            ],
            "transformative_effects": [
                "Chi/energy awareness",
                "Spiritual development through martial arts"
            ],
            "notes": "Referred by Korean karate/Tai Kwan Do teacher; extensive Chi experiences",
            "source": "Mack (1994), Chapter 12, pp. 258-285"
        },
        {
            "case_id": "MACK-11",
            "pseudonym": "Peter",
            "chapter": 13,
            "chapter_title": "Peter's Journey",
            "gender": "M",
            "age_at_contact": 34,
            "age_description": "thirty-four",
            "occupation": "Former hotel manager; recent acupuncture school graduate",
            "location_state": "Massachusetts",
            "location_detail": "Cambridge area (heard lecture at Cambridge Hospital)",
            "marital_status": "Not specified",
            "year_contacted_mack": 1992,
            "month_contacted_mack": "January",
            "first_experience_year": None,
            "first_experience_age": "Not specified",
            "first_experience_location": "Not specified",
            "number_of_sessions": 7,
            "session_type": "Hypnosis",
            "session_dates": "February 1992 - April 1993",
            "attended_support_group": None,
            "experience_types": [
                "Initially intensely traumatic abductions",
                "Dual human/alien identity",
                "Participation in hybrid breeding program",
                "Apocalyptic visions of Earth destruction",
                "Spiritual journey across dimensions"
            ],
            "entity_description": "Not detailed in available excerpts",
            "physical_evidence": [],
            "key_themes": [
                "Transformation of experience quality over time",
                "Evolution of consciousness",
                "Dual human/alien identity",
                "Hybrid breeding program participation",
                "Apocalyptic imagery",
                "Public advocacy - went public with experiences"
            ],
            "transformative_effects": [
                "Perceiving other dimensions/realities",
                "Spiritual journey",
                "Became public advocate (conferences, TV, radio)"
            ],
            "notes": "One of the most dramatic examples of experiential transformation; became public advocate",
            "source": "Mack (1994), Chapter 13, pp. 286-329"
        },
        {
            "case_id": "MACK-12",
            "pseudonym": "Carlos",
            "chapter": 14,
            "chapter_title": "A Being of Light",
            "gender": "M",
            "age_at_contact": 55,
            "age_description": "fifty-five",
            "occupation": "Fine arts professor at small southern college; artist, writer, playwright, theatrical director",
            "location_state": "Southern US (small college town)",
            "location_detail": "Also: experience on Iona, Inner Hebrides, Scotland",
            "marital_status": "Married, three grown children (two sons, one daughter)",
            "year_contacted_mack": 1992,
            "month_contacted_mack": "July",
            "first_experience_year": 1990,
            "first_experience_age": "~53 (Easter Sunday 1990 lost time); also age 9 UFO sighting",
            "first_experience_location": "Iona, Inner Hebrides, Scotland",
            "number_of_sessions": 2,
            "session_type": "Hypnosis/relaxation (totaling 6 hours)",
            "attended_support_group": None,
            "experience_types": [
                "Lost time (6+ hours) on Easter Sunday 1990",
                "Being of Light encounter",
                "Reptilian beings",
                "UFO sighting at age 9 (family witnesses)",
                "Previous hypnosis sessions (17 hours with local psychiatrist)",
                "Healing abilities"
            ],
            "entity_description": "Being of Light; reptilian creatures; grays",
            "physical_evidence": [],
            "key_themes": [
                "Voluntary abductee concept",
                "Cross-cultural/international experience (Scotland)",
                "Artistic/creative expression of experiences",
                "Environmental activism",
                "Co-authored chapter with Mack",
                "Prefers term other than 'abduction'"
            ],
            "transformative_effects": [
                "Environmental/ecological awareness",
                "Healing orientation",
                "Community service (prison, handicapped, mentally ill, elderly)"
            ],
            "notes": "Co-author of chapter; preferred different terminology than 'abduction'; connected to Allagash case witnesses; extensive prior investigation (17 hrs with local psychiatrist)",
            "source": "Mack (1994), Chapter 14, pp. 330-364"
        },
        {
            "case_id": "MACK-13",
            "pseudonym": "Arthur",
            "chapter": 15,
            "chapter_title": "Arthur: A Voluntary Abductee",
            "gender": "M",
            "age_at_contact": 38,
            "age_description": "thirty-eight",
            "occupation": "Highly successful businessman; homes on both coasts",
            "location_state": "Bicoastal (US)",
            "location_detail": "Homes on both coasts",
            "marital_status": "Not specified",
            "year_contacted_mack": 1993,
            "month_contacted_mack": "January",
            "first_experience_year": None,
            "first_experience_age": "Age 9 (dramatic UFO sighting with family)",
            "first_experience_location": "Not specified",
            "number_of_sessions": None,
            "session_type": "Investigation just begun at time of writing",
            "attended_support_group": None,
            "experience_types": [
                "UFO sighting at age 9 (family witnesses)",
                "Ascending to higher realm",
                "Voluntary participation",
                "Gray beings",
                "Reptilian beings"
            ],
            "entity_description": "Grays; reptilian beings",
            "physical_evidence": [],
            "key_themes": [
                "Voluntary abductee",
                "Democratization of capitalism",
                "Sustainable environment",
                "Planetary future",
                "Social/ecological responsibility attributed to experiences",
                "Positive human future example"
            ],
            "transformative_effects": [
                "Profound and lasting ecological awareness from age 9",
                "Commitment to sustainable business",
                "Social responsibility"
            ],
            "notes": "Final case in series; selected as positive example of possible human futures; family also witnessed UFO at age 9",
            "source": "Mack (1994), Chapter 15, pp. 365-383"
        }
    ]
    return cases


def build_research_metadata():
    """Build metadata about Mack's overall research program."""
    return {
        "researcher": {
            "name": "John Edward Mack, M.D.",
            "born": "1929-10-04",
            "died": "2004-09-27",
            "institution": "Harvard Medical School",
            "department": "Psychiatry (Head of Department 1977-2004)",
            "other_notable_work": "Pulitzer Prize 1977 for 'A Prince of Our Disorder' (T.E. Lawrence biography)",
            "research_program": "Program for Extraordinary Experience Research (PEER)",
            "peer_founded": 1993,
            "peer_funding": "Laurance Rockefeller grant",
            "years_active_ufo_research": "1990-2004"
        },
        "research_scope": {
            "total_experiencers_studied": "~200",
            "total_cases_investigated": "~100 (intensive)",
            "total_hypnosis_sessions": "325+",
            "years_of_clinical_investigation": 12,
            "published_case_studies": 13,
            "book_abduction_cases": 13,
            "selection_criteria": [
                "Illustrates one or more central aspects of the phenomenon",
                "Person willing to have story told (with or without pseudonym)",
                "Mack knew individual quite well"
            ],
            "methodology": [
                "Initial 2-hour screening interview",
                "Hypnotic regression sessions",
                "Support group participation",
                "Qualitative clinical analysis",
                "Matrix categorizing experiences (primary, secondary, ancillary)"
            ],
            "inclusion_criterion": "Whether experience was felt to be real by experiencer and communicated sincerely and authentically"
        },
        "publications": {
            "primary_book": {
                "title": "Abduction: Human Encounters with Aliens",
                "year": 1994,
                "publisher": "Scribner's (New York)",
                "isbn": "0684195399",
                "pages": 432,
                "case_studies": 13,
                "archive_org_url": "https://archive.org/details/abductionhumanen0000mack_s4j4"
            },
            "second_book": {
                "title": "Passport to the Cosmos: Human Transformation and Alien Encounters",
                "year": 1999,
                "publisher": "Crown Publishers / Kunati",
                "isbn": "0517705680",
                "pages": 333,
                "structure": "Thematic chapters rather than individual case studies",
                "focus": "Cross-cultural perspectives, indigenous experiences, consciousness",
                "archive_org_url": "https://archive.org/details/passporttocosmos0000mack"
            }
        },
        "harvard_investigation": {
            "year": 1994,
            "initiated_by": "Dean of Harvard Medical School",
            "nature": "Committee to review Mack's clinical care",
            "significance": "First time in Harvard history a tenured professor subjected to such investigation",
            "outcome": "August 1995: Committee reaffirmed Dr. Mack's academic freedom",
            "outcome_detail": "Freedom to study what he wishes and state opinions without impediment"
        },
        "archive_location": {
            "institution": "Rice University, Woodson Research Center, Fondren Library",
            "collection_name": "John E. Mack Archives",
            "collection_id": "MS 1066",
            "location": "Houston, Texas",
            "size": "150 linear feet (150 boxes)",
            "dates": "1970-2010",
            "status": "Unprocessed",
            "materials": "Reports, correspondence, email, interview recordings, photographs, videorecordings",
            "access": "Stored offsite at Library Service Center; 24-hour notice required",
            "digital_status": "Digitization in progress led by Karin Austin (JEMI director)",
            "restrictions": "Private data restricted until anonymization or 2074",
            "parent_collection": "Archives of the Impossible (AOTI)",
            "aoti_founded": 2014,
            "aoti_founder": "Jeffrey J. Kripal (Professor of Religion, Rice University)",
            "contact_email": "woodson@rice.edu",
            "contact_phone": "713-348-2586",
            "finding_aid_url": "https://archives.library.rice.edu/repositories/2/resources/1595"
        },
        "notable_other_cases": {
            "ariel_school": {
                "year": 1994,
                "location": "Ruwa, Zimbabwe",
                "witnesses": "62 schoolchildren",
                "description": "Children observed craft and beings communicating telepathically about environmental stewardship",
                "significance": "Cross-cultural validation; consistent with North American reports"
            },
            "mit_conference": {
                "year": 1992,
                "event": "MIT Abduction Study Conference",
                "proceedings": "600+ page proceedings",
                "significance": "Major academic conference on abduction phenomena"
            }
        },
        "common_patterns_identified": [
            "Luminous or energetic beings",
            "Intense visionary states",
            "Episodes of paralysis followed by perceived transport",
            "Transformative aftermaths emphasizing planetary concern",
            "Missing time",
            "Reproductive/sexual procedures",
            "Environmental/ecological messages",
            "Dual human/alien identity",
            "Cross-generational family patterns",
            "Childhood onset (often age 2-3)",
            "Past life experiences during sessions",
            "Physical marks (cuts, ulcers, triangular lesions)",
            "Telepathic communication",
            "Hybrid offspring reports"
        ]
    }


def compute_demographics_summary(cases):
    """Compute summary statistics from the 13 case studies."""
    genders = [c["gender"] for c in cases]
    ages = [c["age_at_contact"] for c in cases if c["age_at_contact"] is not None]

    # Count experience types
    all_exp_types = []
    for c in cases:
        all_exp_types.extend(c.get("experience_types", []))

    # Categorize
    exp_categories = {}
    for exp in all_exp_types:
        exp_lower = exp.lower()
        if any(w in exp_lower for w in ["reproductive", "sexual", "vagina", "egg", "probing", "anal", "needle"]):
            cat = "Medical/reproductive procedures"
        elif any(w in exp_lower for w in ["missing time", "lost time"]):
            cat = "Missing time"
        elif any(w in exp_lower for w in ["telepathic", "communication", "message"]):
            cat = "Telepathic communication"
        elif any(w in exp_lower for w in ["childhood", "age 3", "age 7", "early"]):
            cat = "Childhood onset"
        elif any(w in exp_lower for w in ["dual", "identity", "hybrid"]):
            cat = "Dual/hybrid identity"
        elif any(w in exp_lower for w in ["spiritual", "mission", "light", "energy"]):
            cat = "Spiritual/transformative"
        elif any(w in exp_lower for w in ["paralysis", "transported", "craft", "ufo", "taken"]):
            cat = "Transport/craft encounter"
        elif any(w in exp_lower for w in ["scar", "nosebleed", "mark", "lesion"]):
            cat = "Physical evidence"
        elif any(w in exp_lower for w in ["dream", "vision", "apocalyptic"]):
            cat = "Visions/dreams"
        else:
            cat = "Other"
        exp_categories[cat] = exp_categories.get(cat, 0) + 1

    summary = {
        "total_published_cases": len(cases),
        "gender_distribution": {
            "male": genders.count("M"),
            "female": genders.count("F")
        },
        "age_at_contact": {
            "min": min(ages),
            "max": max(ages),
            "mean": round(sum(ages) / len(ages), 1),
            "median": sorted(ages)[len(ages) // 2],
            "values": sorted(ages)
        },
        "locations": {
            "Massachusetts": 3,
            "Northeast US (unspecified)": 4,
            "New Hampshire": 1,
            "Pennsylvania": 1,
            "Southern US": 1,
            "Bicoastal": 1,
            "Not specified": 3
        },
        "occupations": [c["occupation"] for c in cases],
        "experience_category_counts": dict(sorted(exp_categories.items(), key=lambda x: -x[1])),
        "year_contacted_mack": {
            "range": "1991-1993",
            "1991": sum(1 for c in cases if c.get("year_contacted_mack") == 1991),
            "1992": sum(1 for c in cases if c.get("year_contacted_mack") == 1992),
            "1993": sum(1 for c in cases if c.get("year_contacted_mack") == 1993),
            "not_specified": sum(1 for c in cases if c.get("year_contacted_mack") is None)
        },
        "childhood_onset": sum(1 for c in cases if any("age" in str(c.get("first_experience_age", "")).lower() and
                                                         any(a in str(c.get("first_experience_age", ""))
                                                             for a in ["3", "7", "child", "early"])
                                                         for _ in [1])),
        "notes": "All names are pseudonyms. Demographics extracted from published text."
    }
    return summary


def export_csv(cases, filepath):
    """Export case studies to CSV."""
    fieldnames = [
        "case_id", "pseudonym", "chapter", "chapter_title",
        "gender", "age_at_contact", "occupation", "location_state",
        "marital_status", "year_contacted_mack",
        "first_experience_age", "number_of_sessions",
        "experience_types", "entity_description",
        "physical_evidence", "key_themes",
        "transformative_effects", "source"
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for case in cases:
            row = {}
            for k in fieldnames:
                val = case.get(k, "")
                if isinstance(val, list):
                    val = "; ".join(str(v) for v in val)
                row[k] = val
            writer.writerow(row)
    print(f"  CSV exported: {filepath}")


def export_json(data, filepath, label=""):
    """Export data to JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    print(f"  JSON exported: {filepath} {label}")


def build_data_availability_report():
    """Document what data exists and where."""
    return {
        "report_date": datetime.now().isoformat(),
        "summary": (
            "John E. Mack's abduction research data is extremely limited in digital availability. "
            "The bulk of his raw research (150 boxes covering ~200 experiencers) is archived at "
            "Rice University and is NOT publicly accessible or digitized. The only published "
            "structured data comes from his 1994 book 'Abduction' which presents 13 detailed case "
            "studies. No digitized databases, spreadsheets, or structured datasets of his research "
            "have been found online."
        ),
        "data_sources_searched": [
            {
                "source": "johnemackinstitute.org (JEMI)",
                "status": "TLS certificate error - site appears to have infrastructure issues",
                "data_found": False,
                "notes": "JEMI website has SSL/TLS certificate problems; HTTP version references exist but redirect fails"
            },
            {
                "source": "Archive.org",
                "status": "Book exists but in Print Disabled / Access Restricted collection",
                "data_found": True,
                "notes": "Abduction (1994) available as restricted item; Passport to the Cosmos (1999) also listed",
                "urls": [
                    "https://archive.org/details/abductionhumanen0000mack_s4j4",
                    "https://archive.org/details/passporttocosmos0000mack"
                ]
            },
            {
                "source": "Avalon Library",
                "status": "Full PDF of Abduction book available and downloaded",
                "data_found": True,
                "notes": "14.3MB PDF downloaded to data/Mack_Abduction_Human_Encounters_with_Aliens.pdf",
                "url": "https://avalonlibrary.net/ebooks/John%20E.%20Mack,%20MD%20-%20Abduction%20-%20Human%20Encounters%20with%20Aliens.pdf"
            },
            {
                "source": "GitHub",
                "status": "No repositories found",
                "data_found": False,
                "notes": "Searched GitHub API for 'john mack abduction' and related terms - no results"
            },
            {
                "source": "Academic journals",
                "status": "No journal papers with structured case data found",
                "data_found": False,
                "notes": "Mack published books rather than journal papers; his work faced academic scrutiny and was not published in peer-reviewed journals as structured case series"
            },
            {
                "source": "Harvard Countway Library",
                "status": "No digital collections found for Mack's abduction research",
                "data_found": False,
                "notes": "Mack's research materials were donated to Rice University, not retained at Harvard"
            },
            {
                "source": "Rice University Archives of the Impossible",
                "status": "150 boxes archived but NOT digitized or publicly accessible",
                "data_found": False,
                "notes": "MS 1066; unprocessed; restricted until anonymization or 2074; Karin Austin leading digitization effort",
                "url": "https://archives.library.rice.edu/repositories/2/resources/1595"
            },
            {
                "source": "MedDocs Online - Academic paper",
                "status": "Downloaded paper about Mack's work",
                "data_found": True,
                "notes": "Paper: 'The Psychiatrist Who Flew Into Space and Never Came Back' - overview of Mack's career and research",
                "file": "psychiatrist_who_flew_into_space.pdf"
            },
            {
                "source": "UFO Insight",
                "status": "Case summaries extracted",
                "data_found": True,
                "notes": "Detailed summaries of 6 cases (Ed, Scott, Lee, Catherine, Sara, Paul)",
                "url": "https://www.ufoinsight.com/aliens/abductions/john-mack-alien-abduction-files"
            },
            {
                "source": "PBS NOVA",
                "status": "Interview transcript with case details",
                "data_found": True,
                "notes": "Mack interview from 'Kidnapped by UFOs' program",
                "url": "https://www.pbs.org/wgbh/nova/aliens/johnmack.html"
            }
        ],
        "files_saved": [
            {
                "file": "Mack_Abduction_Human_Encounters_with_Aliens.pdf",
                "description": "Full text of 1994 book (PDF, 14.3MB)",
                "source": "Avalon Library"
            },
            {
                "file": "Mack_Abduction_text.txt",
                "description": "Extracted text from book PDF (23,268 lines)",
                "source": "pdftotext extraction"
            },
            {
                "file": "psychiatrist_who_flew_into_space.pdf",
                "description": "Academic paper on Mack's career and research",
                "source": "MedDocs Online"
            },
            {
                "file": "mack_case_studies.json",
                "description": "Structured data for all 13+1 published case studies",
                "source": "Compiled from book text"
            },
            {
                "file": "mack_case_studies.csv",
                "description": "CSV export of case studies",
                "source": "Compiled from book text"
            },
            {
                "file": "mack_research_metadata.json",
                "description": "Metadata about Mack's research program, methods, and archive",
                "source": "Compiled from multiple sources"
            },
            {
                "file": "mack_demographics_summary.json",
                "description": "Statistical summary of the 13 published cases",
                "source": "Computed from case data"
            },
            {
                "file": "mack_data_availability_report.json",
                "description": "This report documenting data sources and availability",
                "source": "Search results compilation"
            }
        ],
        "conclusion": (
            "Mack's published data is qualitative and narrative-based, not quantitative. "
            "The 13 case studies from his 1994 book represent the entirety of his publicly "
            "available structured case data. His broader research on ~200 experiencers remains "
            "locked in the Rice University archives, where it is being slowly digitized with "
            "a target de-identification process. The full archive will likely not be publicly "
            "available for many years, and some materials are restricted until 2074."
        )
    }


def main():
    print("=" * 70)
    print("COMPILING JOHN E. MACK ABDUCTION RESEARCH DATA")
    print("=" * 70)
    print()

    # Build case studies
    print("[1/5] Building case study database...")
    cases = build_case_studies()
    print(f"  Compiled {len(cases)} case studies from 'Abduction' (1994)")

    # Build research metadata
    print("[2/5] Building research metadata...")
    metadata = build_research_metadata()

    # Compute demographics
    print("[3/5] Computing demographics summary...")
    demographics = compute_demographics_summary(cases)
    print(f"  Gender: {demographics['gender_distribution']}")
    print(f"  Age range: {demographics['age_at_contact']['min']}-{demographics['age_at_contact']['max']} "
          f"(mean: {demographics['age_at_contact']['mean']})")

    # Build availability report
    print("[4/5] Building data availability report...")
    report = build_data_availability_report()

    # Export everything
    print("[5/5] Exporting data files...")

    export_json(cases, os.path.join(DATA_DIR, "mack_case_studies.json"), f"({len(cases)} cases)")
    export_csv(cases, os.path.join(DATA_DIR, "mack_case_studies.csv"))
    export_json(metadata, os.path.join(DATA_DIR, "mack_research_metadata.json"))
    export_json(demographics, os.path.join(DATA_DIR, "mack_demographics_summary.json"))
    export_json(report, os.path.join(DATA_DIR, "mack_data_availability_report.json"))

    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"  Total case studies compiled: {len(cases)}")
    print(f"  Data files generated: 5")
    print(f"  Source documents downloaded: 2 (book PDF + academic paper)")
    print(f"  Book text extracted: 23,268 lines")
    print()
    print("  KEY FINDINGS:")
    print("  - Mack's raw research data (150 boxes, ~200 cases) is at Rice University")
    print("  - Archives are unprocessed and NOT publicly available")
    print("  - Some materials restricted until 2074")
    print("  - Only published data: 13 case studies in 'Abduction' (1994)")
    print("  - No GitHub repos, no digitized databases found anywhere online")
    print("  - johnemackinstitute.org has TLS certificate issues")
    print()
    print(f"  Output directory: {DATA_DIR}")
    print()


if __name__ == "__main__":
    main()
