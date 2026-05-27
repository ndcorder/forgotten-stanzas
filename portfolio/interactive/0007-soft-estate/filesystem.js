/**
 * filesystem.js — The narrative heart of Soft Estate
 *
 * Every file, folder, email, browser entry, and system artifact
 * that constitutes Elena Marsh's digital remains.
 *
 * The deceased: Elena Victoria Marsh
 * Born: March 12, 1991
 * Died: November 17, 2023 (age 32)
 *
 * Clock frozen at 3:47 AM, November 18, 2023
 * Last actual activity: ~3:43 AM
 */

var FileSystem = {

  root: {
    type: 'folder',
    name: 'Macintosh HD',
    children: {
      'Users': {
        type: 'folder',
        name: 'Users',
        children: {
          'elena.marsh': {
            type: 'folder',
            name: 'elena.marsh',
            children: {

              /* ─── Desktop ─── The chaos of a working life interrupted */

              'Desktop': {
                type: 'folder',
                name: 'Desktop',
                icon: 'folder-desktop',
                children: {

                  'project_meridian': {
                    type: 'folder',
                    name: 'project_meridian',
                    children: {

                      'README.txt': {
                        type: 'file',
                        name: 'README.txt',
                        icon: 'file-txt',
                        modified: '2023-11-14T22:31:00',
                        size: 1247,
                        content: [
                          'PROJECT MERIDIAN — MASTER DOCUMENT',
                          '========================================',
                          '',
                          'Client: Meridian Health Systems',
                          'Lead: Elena Marsh',
                          'Status: In Development',
                          'Deadline: December 1, 2023',
                          '',
                          'DELIVERABLES:',
                          '├─ Brand identity system',
                          '├─ Patient portal UX (mobile-first)',
                          '├─ Internal signage package',
                          '└─ Accessibility audit (WCAG 2.1)',
                          '',
                          'NOTES:',
                          'See individual folders for assets.',
                          'Karen wants the "warm but clinical" feel.',
                          'Third round of revisions on the logo.',
                          'She keeps asking for "more blue" which is not a color note.',
                          '',
                          'TO DO:',
                          '- [ ] Finalize color palette',
                          '- [ ] Patient portal wireframes (v3)',
                          '- [ ] Send invoice #4',
                          '- [x] Kickoff meeting notes',
                          '- [ ] Accessibility report'
                        ].join('\n')
                      },

                      'brand_guidelines_v3.pdf': {
                        type: 'file',
                        name: 'brand_guidelines_v3.pdf',
                        icon: 'file-pdf',
                        modified: '2023-11-12T19:45:00',
                        size: 4210240,
                        content: null,
                        metadata: {
                          pages: 47,
                          title: 'Meridian Health Systems — Brand Guidelines v3',
                          author: 'Elena Marsh',
                          lastEditedBy: 'elena.marsh',
                          pdfVersion: '1.7'
                        }
                      },

                      'client_feedback': {
                        type: 'folder',
                        name: 'client_feedback',
                        children: {

                          'karen_notes_nov8.eml': {
                            type: 'file',
                            name: 'karen_notes_nov8.eml',
                            icon: 'file-email',
                            modified: '2023-11-08T14:22:00',
                            size: 3891,
                            content: [
                              'From: Karen Whitfield <k.whitfield@meridianhealth.org>',
                              'To: Elena Marsh <elena.marsh@tidaldesign.co>',
                              'Date: November 8, 2023 2:22 PM',
                              'Subject: Re: Brand Guidelines v2 — Notes',
                              '',
                              'Hi Elena,',
                              '',
                              'Thanks for the revisions. A few thoughts:',
                              '',
                              '1. The blue is still wrong. I know I keep saying this but it needs to be',
                              '   WARMER. Not warmer-warm, but warm in the way that a hospital doesn\'t',
                              '   feel warm, you know?',
                              '',
                              '2. The patient portal mockups are much better. Can we make the appointment',
                              '   booking FEWER clicks? My mother can barely use her iPad.',
                              '',
                              '3. Love the accessibility features. Seriously. This is why we hired you.',
                              '',
                              '4. The internal signage — can the fonts be bigger? Like, uncomfortably big?',
                              '   We have elderly patients who are scared and not wearing their glasses.',
                              '',
                              '5. I showed the board and they want to see one more round before sign-off.',
                              '   I know the deadline is tight. I\'m sorry.',
                              '',
                              'Can we meet Thursday the 16th? I cleared my afternoon.',
                              '',
                              'Best,',
                              'Karen',
                              '',
                              '--',
                              'Karen Whitfield',
                              'Director of Communications',
                              'Meridian Health Systems',
                              '(she/her)'
                            ].join('\n')
                          },

                          'karen_notes_nov14.eml': {
                            type: 'file',
                            name: 'karen_notes_nov14.eml',
                            icon: 'file-email',
                            modified: '2023-11-14T16:38:00',
                            size: 1847,
                            content: [
                              'From: Karen Whitfield <k.whitfield@meridianhealth.org>',
                              'To: Elena Marsh <elena.marsh@tidaldesign.co>',
                              'Date: November 14, 2023 4:38 PM',
                              'Subject: Re: Thursday meeting — rescheduling?',
                              '',
                              'Elena, are you okay? You didn\'t make the meeting.',
                              '',
                              'I tried calling. Your phone went straight to voicemail.',
                              '',
                              'The deadline is December 1st. I need to know if you can still deliver.',
                              'If you\'re dealing with something, just tell me. I can extend if needed.',
                              '',
                              'Please just let me know you\'re alright.',
                              '',
                              'Karen'
                            ].join('\n')
                          }
                        }
                      },

                      'invoices': {
                        type: 'folder',
                        name: 'invoices',
                        children: {

                          'invoice_004_draft.txt': {
                            type: 'file',
                            name: 'invoice_004_draft.txt',
                            icon: 'file-txt',
                            modified: '2023-11-14T23:12:00',
                            size: 876,
                            content: [
                              'INVOICE #004 — DRAFT',
                              '====================',
                              'Tidal Design Studio',
                              'Elena Marsh, Principal',
                              '',
                              'Client: Meridian Health Systems',
                              'Project: Brand Identity & Patient Portal',
                              'Period: October 15 — November 14, 2023',
                              '',
                              'DESCRIPTION                          HOURS    RATE      AMOUNT',
                              '\u2500'.repeat(64),
                              'Brand guidelines revision (v3)         18     $95       $1,710.00',
                              'Patient portal wireframes (v2\u2192v3)      22     $95       $2,090.00',
                              'Accessibility audit (partial)           8     $95       $   760.00',
                              'Client meetings                         3     $95       $   285.00',
                              '',
                              'SUBTOTAL: $4,845.00',
                              'TAX:         $0.00',
                              'TOTAL:       $4,845.00',
                              '',
                              'Payment terms: Net 30',
                              'Account: TD Business Checking ****7291',
                              '',
                              '[NOT SENT \u2014 DRAFT]'
                            ].join('\n')
                          },

                          'invoice_003_paid.pdf': {
                            type: 'file',
                            name: 'invoice_003_paid.pdf',
                            icon: 'file-pdf',
                            modified: '2023-10-15T10:00:00',
                            size: 245000,
                            content: null,
                            metadata: {
                              status: 'PAID',
                              amount: '$3,800.00',
                              paidDate: '2023-10-29'
                            }
                          }
                        }
                      }
                    }
                  },

                  'grocery_list.txt': {
                    type: 'file',
                    name: 'grocery_list.txt',
                    icon: 'file-txt',
                    modified: '2023-11-17T11:34:00',
                    size: 412,
                    content: [
                      'GROCERY \u2014 WEEK OF 11/17',
                      '========================',
                      '',
                      'almond milk (unsweetened)',
                      'blueberries (frozen is fine)',
                      'chicken breasts',
                      'spinach',
                      'brown rice',
                      'olive oil (running low)',
                      'dish soap',
                      'paper towels',
                      'candles \u2014 the ones from sprouts, lavender',
                      '    \u2192 the OTHER lavender, not the sleep one',
                      'batteries (AA)',
                      'cat food (wet \u2014 salmon) \u2190 IMPORTANT',
                      '',
                      'maybe:',
                      '  - crackers?',
                      '  - that cheese diane liked',
                      '  - flowers for the table',
                      '',
                      'DO NOT FORGET THE CAT FOOD'
                    ].join('\n')
                  },

                  'job_posting_screenshot.png': {
                    type: 'file',
                    name: 'job_posting_screenshot.png',
                    icon: 'file-image',
                    modified: '2023-11-10T01:23:00',
                    size: 389120,
                    content: null,
                    metadata: {
                      width: 1440,
                      height: 900,
                      exif: {
                        created: '2023-11-10T01:23:00',
                        software: 'macOS Screenshot'
                      }
                    }
                  },

                  'dentist_reminder.ics': {
                    type: 'file',
                    name: 'dentist_reminder.ics',
                    icon: 'file-cal',
                    modified: '2023-11-01T09:00:00',
                    size: 412,
                    content: [
                      'BEGIN:VCALENDAR',
                      'BEGIN:VEVENT',
                      'DTSTART:20231205T140000',
                      'DTEND:20231205T150000',
                      'SUMMARY:Dentist \u2014 Dr. Patel',
                      'LOCATION:Westlake Dental, 445 Lake St',
                      'DESCRIPTION:6-month cleaning. They sent a reminder card.',
                      ' Insurance card is in the drawer.',
                      'END:VEVENT',
                      'END:VCALENDAR'
                    ].join('\n')
                  }
                }
              },

              /* ─── Documents ─── The architecture of an adult life */

              'Documents': {
                type: 'folder',
                name: 'Documents',
                icon: 'folder-documents',
                children: {

                  'work': {
                    type: 'folder',
                    name: 'work',
                    children: {
                      'tidal_design': {
                        type: 'folder',
                        name: 'tidal_design',
                        children: {

                          'contract_meridian.pdf': {
                            type: 'file',
                            name: 'contract_meridian.pdf',
                            icon: 'file-pdf',
                            modified: '2023-08-22T10:15:00',
                            size: 156000,
                            content: null,
                            metadata: {
                              title: 'Service Agreement \u2014 Meridian Health Systems',
                              signedDate: '2023-08-22',
                              totalValue: '$18,000'
                            }
                          },

                          'business_plan_2023.txt': {
                            type: 'file',
                            name: 'business_plan_2023.txt',
                            icon: 'file-txt',
                            modified: '2023-09-03T15:22:00',
                            size: 2341,
                            content: [
                              'TIDAL DESIGN STUDIO \u2014 2023 PLAN',
                              '================================',
                              '',
                              'OK. Second year. Here we go.',
                              '',
                              'GOALS:',
                              '\u2022 4-5 steady clients (currently: 3)',
                              '\u2022 Monthly revenue: $6,500+',
                              '\u2022 Hire a part-time junior by Q3',
                              '\u2022 Move out of the apartment into a real office space',
                              '',
                              'CURRENT CLIENTS:',
                              '1. Meridian Health Systems \u2014 $18K contract (brand + portal)',
                              '2. Back Creek Brewery \u2014 ongoing, ~$1,200/mo',
                              '3. Ellery & Associates Law \u2014 website redesign, almost done',
                              '',
                              'PIPELINE:',
                              '- Greenway Parks Dept (waiting on RFP)',
                              '- That woman from the networking thing? Solar company?',
                              '- Denise\'s friend who needs a restaurant site',
                              '',
                              'FINANCES:',
                              'Savings: $4,200 (don\'t touch)',
                              'Business account: ~$7,800',
                              'Personal: rent is due the 1st, always the 1st',
                              '',
                              'NOTES TO SELF:',
                              '- Stop underpricing. You\'re good at this.',
                              '- The junior hire would change everything.',
                              '- Talk to Marcus about the LLC tax thing.',
                              '- Call Mom. She worries.',
                              '',
                              'REVENUE TARGETS:',
                              'Q1: $12,000 \u2713',
                              'Q2: $15,000 \u2713',
                              'Q3: $14,000 (slightly under)',
                              'Q4: $18,000 (on track with Meridian)',
                              '',
                              'TOTAL PROJECTED: ~$59,000',
                              'After expenses: ~$41,000',
                              'It\'s not tech-bro money but it\'s mine.'
                            ].join('\n')
                          }
                        }
                      }
                    }
                  },

                  'personal': {
                    type: 'folder',
                    name: 'personal',
                    children: {

                      'lease_agreement.pdf': {
                        type: 'file',
                        name: 'lease_agreement.pdf',
                        icon: 'file-pdf',
                        modified: '2022-06-01T12:00:00',
                        size: 312000,
                        content: null,
                        metadata: {
                          title: 'Residential Lease Agreement',
                          address: '1428 Ridgeway Ave, Apt 3B',
                          termStart: '2022-07-01',
                          termEnd: '2024-06-30',
                          monthlyRent: '$1,350'
                        }
                      },

                      'insurance_cards.pdf': {
                        type: 'file',
                        name: 'insurance_cards.pdf',
                        icon: 'file-pdf',
                        modified: '2023-01-15T08:00:00',
                        size: 89000,
                        content: null
                      },

                      'recipes': {
                        type: 'folder',
                        name: 'recipes',
                        children: {
                          'dianas_bread_pudding.txt': {
                            type: 'file',
                            name: 'dianas_bread_pudding.txt',
                            icon: 'file-txt',
                            modified: '2023-09-20T19:45:00',
                            size: 1123,
                            content: [
                              'DIANA\'S BREAD PUDDING',
                              '=====================',
                              '',
                              'From Mom\'s recipe box, transcribed by Diane',
                              '(Diane added the bourbon. Mom pretends she didn\'t.)',
                              '',
                              '1 loaf stale French bread, torn into pieces',
                              '2 cups whole milk',
                              '1 cup heavy cream',
                              '3 eggs',
                              '1 cup sugar',
                              '2 tsp vanilla',
                              '1 tsp cinnamon',
                              '1/2 tsp nutmeg',
                              'Pinch of salt',
                              '1/2 cup raisins (optional, Diane says mandatory)',
                              '3 tbsp bourbon (optional, Diane says mandatory)',
                              '',
                              'Butter a 9x13 dish. Preheat 350\u00b0.',
                              '',
                              'Soak bread in milk/cream for 15 min.',
                              'Mix everything else. Combine. Pour into dish.',
                              'Bake 45-50 min until set and golden.',
                              '',
                              'SAUCE:',
                              '1 stick butter',
                              '1 cup brown sugar',
                              '1 egg',
                              'Bourbon to taste (Diane: "to taste" means 4 tbsp minimum)',
                              '',
                              'Melt butter and sugar. Whisk in egg over low heat until thick.',
                              'Add bourbon. Pour over warm pudding.',
                              '',
                              'Serve at Thanksgiving. Always at Thanksgiving.',
                              'Elena, I\'m putting this in your folder because you keep asking.',
                              'Make it this year.',
                              '\u2014 D'
                            ].join('\n')
                          }
                        }
                      }
                    }
                  }
                }
              },

              /* ─── Downloads ─── The quiet archaeology of late nights */

              'Downloads': {
                type: 'folder',
                name: 'Downloads',
                icon: 'folder-downloads',
                children: {
                  'smoothie_recipe.pdf': {
                    type: 'file',
                    name: 'smoothie_recipe.pdf',
                    icon: 'file-pdf',
                    modified: '2023-11-16T08:12:00',
                    size: 45000,
                    content: null,
                    metadata: { source: 'Pinterest' }
                  },
                  'budget_template.xlsx': {
                    type: 'file',
                    name: 'budget_template.xlsx',
                    icon: 'file-spreadsheet',
                    modified: '2023-10-28T14:33:00',
                    size: 23000,
                    content: null
                  },
                  'Apt3B_lease_renewal.pdf': {
                    type: 'file',
                    name: 'Apt3B_lease_renewal.pdf',
                    icon: 'file-pdf',
                    modified: '2023-11-15T09:22:00',
                    size: 178000,
                    content: null,
                    metadata: {
                      title: 'Lease Renewal Offer \u2014 Apt 3B',
                      newRent: '$1,425/mo',
                      notes: 'increase :( but still cheaper than moving'
                    }
                  }
                }
              },

              /* ─── Pictures ─── What she chose to keep */

              'Pictures': {
                type: 'folder',
                name: 'Pictures',
                icon: 'folder-pictures',
                children: {

                  'vacation_2023': {
                    type: 'folder',
                    name: 'vacation_2023',
                    children: {
                      'IMG_0847.jpg': {
                        type: 'file',
                        name: 'IMG_0847.jpg',
                        icon: 'file-image',
                        modified: '2023-07-14T16:23:11',
                        size: 3421000,
                        content: null,
                        metadata: {
                          width: 4032,
                          height: 3024,
                          camera: 'iPhone 13',
                          exif: {
                            dateTimeOriginal: '2023-07-14T16:23:11',
                            latitude: '44.2734',
                            longitude: '-68.3215',
                            location: 'Acadia National Park, ME',
                            flash: false,
                            exposure: '1/120',
                            aperture: 'f/1.6',
                            iso: 32
                          },
                          description: 'Sunset over the Atlantic. The rocks were warm.'
                        }
                      },
                      'IMG_0851.jpg': {
                        type: 'file',
                        name: 'IMG_0851.jpg',
                        icon: 'file-image',
                        modified: '2023-07-14T18:47:03',
                        size: 2890000,
                        content: null,
                        metadata: {
                          width: 4032,
                          height: 3024,
                          camera: 'iPhone 13',
                          exif: {
                            dateTimeOriginal: '2023-07-14T18:47:03',
                            location: 'Acadia National Park, ME',
                            flash: false
                          },
                          description: 'Diane making that face. The lobster was NOT that big.'
                        }
                      },
                      'IMG_0863.jpg': {
                        type: 'file',
                        name: 'IMG_0863.jpg',
                        icon: 'file-image',
                        modified: '2023-07-15T09:12:44',
                        size: 3120000,
                        content: null,
                        metadata: {
                          width: 4032,
                          height: 3024,
                          camera: 'iPhone 13',
                          exif: {
                            dateTimeOriginal: '2023-07-15T09:12:44',
                            location: 'Acadia National Park, ME'
                          },
                          description: 'Morning fog on the trail. She wanted to go higher.'
                        }
                      }
                    }
                  },

                  'cat': {
                    type: 'folder',
                    name: 'cat',
                    children: {
                      'IMG_1247.jpg': {
                        type: 'file',
                        name: 'IMG_1247.jpg',
                        icon: 'file-image',
                        modified: '2023-11-11T07:04:22',
                        size: 2150000,
                        content: null,
                        metadata: {
                          width: 4032,
                          height: 3024,
                          camera: 'iPhone 13',
                          exif: {
                            dateTimeOriginal: '2023-11-11T07:04:22',
                            location: 'Home \u2014 1428 Ridgeway Ave'
                          },
                          description: 'Mochi on the windowsill. November light.'
                        }
                      },
                      'mochi_sleeping.jpg': {
                        type: 'file',
                        name: 'mochi_sleeping.jpg',
                        icon: 'file-image',
                        modified: '2023-10-20T22:15:00',
                        size: 1980000,
                        content: null,
                        metadata: {
                          width: 4032,
                          height: 3024,
                          camera: 'iPhone 13',
                          exif: {
                            dateTimeOriginal: '2023-10-20T22:15:00',
                            location: 'Home \u2014 1428 Ridgeway Ave'
                          },
                          description: 'Curled up in the blue blanket. She sleeps like a croissant.'
                        }
                      }
                    }
                  },

                  'screenshots': {
                    type: 'folder',
                    name: 'screenshots',
                    children: {}
                  },

                  'nov_17': {
                    type: 'folder',
                    name: 'nov_17',
                    icon: 'folder-smart',
                    children: {
                      'IMG_1403.jpg': {
                        type: 'file',
                        name: 'IMG_1403.jpg',
                        icon: 'file-image',
                        modified: '2023-11-17T15:47:33',
                        size: 4012000,
                        content: null,
                        metadata: {
                          width: 3024,
                          height: 4032,
                          camera: 'iPhone 13',
                          exif: {
                            dateTimeOriginal: '2023-11-17T15:47:33',
                            location: 'Home \u2014 1428 Ridgeway Ave',
                            flash: false,
                            exposure: '1/60',
                            aperture: 'f/1.6',
                            iso: 250,
                            facing: 'back'
                          },
                          description: 'The table. Before anyone arrived. Just the plates.'
                        }
                      },
                      'IMG_1404.jpg': {
                        type: 'file',
                        name: 'IMG_1404.jpg',
                        icon: 'file-image',
                        modified: '2023-11-18T03:47:12',
                        size: 3850000,
                        content: null,
                        metadata: {
                          width: 3024,
                          height: 4032,
                          camera: 'iPhone 13',
                          exif: {
                            dateTimeOriginal: '2023-11-18T03:47:12',
                            location: 'Home \u2014 1428 Ridgeway Ave',
                            flash: false,
                            exposure: '1/15',
                            aperture: 'f/1.6',
                            iso: 800,
                            facing: 'front'
                          },
                          description: 'The last photo on the camera roll. She\'s smiling.'
                        }
                      }
                    }
                  }
                }
              },

              'Music': {
                type: 'folder',
                name: 'Music',
                icon: 'folder',
                children: {}
              },

              'Movies': {
                type: 'folder',
                name: 'Movies',
                icon: 'folder',
                children: {}
              },

              /* ─── dont_open ─── The forty-seven drafts she could never send */

              'dont_open': {
                type: 'folder',
                name: 'dont_open',
                children: {

                  'untitled_01.txt': {
                    type: 'file',
                    name: 'untitled_01.txt',
                    icon: 'file-txt',
                    modified: '2023-11-02T23:48:00',
                    size: 342,
                    content: 'Diane,\n\nI need to tell you something and I don\'t know how. Every time I try to say it the words come out wrong or I chicken out or I convince myself it doesn\'t matter. But it does matter. You deserve to know.\n\nI\'m sorry. For everything I\'m about to be sorry for.\n\nE'
                  },

                  'untitled_02.txt': {
                    type: 'file',
                    name: 'untitled_02.txt',
                    icon: 'file-txt',
                    modified: '2023-11-03T00:14:00',
                    size: 567,
                    content: 'Diane,\n\nThere\'s something I\'ve been dealing with and I haven\'t told anyone. Not you, not Mom, not Marcus. That\'s not fair to you especially. You\'ve been nothing but good to me and I keep pretending everything is fine.\n\nIt\'s not fine. I\'m not fine.\n\nBut I don\'t know how to say the thing I need to say without making it about me, and it\'s not about me, it\'s about you, and us, and how you deserve a sister who doesn\'t\u2014\n\n[file continues]'
                  },

                  'untitled_03.txt': {
                    type: 'file',
                    name: 'untitled_03.txt',
                    icon: 'file-txt',
                    modified: '2023-11-03T00:31:00',
                    size: 201,
                    content: 'D,\n\nI keep starting these over. I\'m going to just write it plain.\n\nI\'m sick. Not like a cold. Like\u2014\n\nI can\'t even write it to my own sister.\n\nForget it.'
                  },

                  'untitled_04.txt': {
                    type: 'file',
                    name: 'untitled_04.txt',
                    icon: 'file-txt',
                    modified: '2023-11-03T01:02:00',
                    size: 423,
                    content: 'Mom,\n\nI should have told you sooner. I know you\'ll be scared. I know you\'ll want to fix it. You can\'t fix this, Mom. Nobody can. That\'s why I didn\'t tell you.\n\nBut you\'re going to find out and I\'d rather it come from me.\n\nI love you. You gave me a good life. You did everything right.\n\nElena'
                  },

                  'untitled_07.txt': {
                    type: 'file',
                    name: 'untitled_07.txt',
                    icon: 'file-txt',
                    modified: '2023-11-05T01:17:00',
                    size: 389,
                    content: 'Diane,\n\nThe doctors say 6-8 months if the treatment doesn\'t work. It probably won\'t work. They said "refractory" which is a word I had to look up and I wish I hadn\'t.\n\nI found out in September. I\'ve known this whole time. I kept working. I kept making plans. I made grocery lists, Diane. I bought cat food. I made a dentist appointment for December.\n\nI don\'t know how to be someone who is dying and also someone who needs milk.\n\nE'
                  },

                  'untitled_12.txt': {
                    type: 'file',
                    name: 'untitled_12.txt',
                    icon: 'file-txt',
                    modified: '2023-11-07T02:45:00',
                    size: 287,
                    content: 'To whoever finds this laptop:\n\nMy name is Elena Victoria Marsh. I\'m 32. I have a cat named Mochi who needs wet food (salmon only, she\'s picky) and a window to sit in.\n\nPlease find Diane. She\'s my sister. She\'ll know what to do.\n\nThe work files on the desktop \u2014 finish the Meridian project if you can. Karen is counting on it. Her email is in the client feedback folder.\n\nThank you.\n\n\u2014E'
                  },

                  'untitled_18.txt': {
                    type: 'file',
                    name: 'untitled_18.txt',
                    icon: 'file-txt',
                    modified: '2023-11-09T23:58:00',
                    size: 534,
                    content: 'Diane,\n\nI keep thinking about Acadia. That morning on the trail when you wanted to go higher and I said I was tired. I wasn\'t tired. I was scared I\'d get dizzy and you\'d ask why.\n\nYou said "we can just sit here then" and you sat with me on that rock and we watched the fog clear and you didn\'t ask for a reason and I almost told you everything right then.\n\nI should have told you everything right then.\n\nYou\'re the best person I know, Diane. You have been since we were kids and you punched that boy for calling me weird. I was weird. You didn\'t care.\n\nI need you to not be weird about this when you find out.\nI need you to just keep being my sister.\nThat\'s all I need.\n\nE'
                  },

                  'untitled_24.txt': {
                    type: 'file',
                    name: 'untitled_24.txt',
                    icon: 'file-txt',
                    modified: '2023-11-11T03:22:00',
                    size: 167,
                    content: 'Mom and Dad,\n\nI saved the good blankets for you. They\'re in the cedar chest at the foot of my bed. Diane will probably try to take them. Don\'t let her.\n\nThe lease runs through June. The landlord is nice. His name is Gordon.\n\nMochi likes to sleep on the blue blanket. Don\'t take the blue blanket.\n\nI love you both so much it makes this harder.\n\nYour daughter,\nElena'
                  },

                  'untitled_31.txt': {
                    type: 'file',
                    name: 'untitled_31.txt',
                    icon: 'file-txt',
                    modified: '2023-11-13T02:04:00',
                    size: 298,
                    content: 'Marcus,\n\nYou were right about the LLC thing. I should have listened.\n\nAlso I owe you dinner. Still owe you dinner from July.\n\nYou\'re a good friend. Thanks for not making the freelance thing weird.\n\nIf Diane reaches out, just be patient with her. She processes things by being angry. It\'s not about you.\n\n\u2014E\n\nPS: The ramen place on 5th. That\'s where you should go. Get the tonkotsu.'
                  },

                  'untitled_38.txt': {
                    type: 'file',
                    name: 'untitled_38.txt',
                    icon: 'file-txt',
                    modified: '2023-11-15T01:49:00',
                    size: 245,
                    content: 'Karen,\n\nI\'m sorry I missed the meeting. I\'m sorry about everything being late.\n\nYou were right to hire me. The work is good. Please don\'t think the work isn\'t good because I fell apart.\n\nFinish it with someone else. The brand guide is 90% there. Just needs the blue you keep asking for.\n\nYou\'ll know it when you see it.\n\n\u2014Elena Marsh\nTidal Design Studio'
                  },

                  'untitled_44.txt': {
                    type: 'file',
                    name: 'untitled_44.txt',
                    icon: 'file-txt',
                    modified: '2023-11-16T03:11:00',
                    size: 93,
                    content: 'last one\n\ni just wanted someone to know me\nall of me\nthe before and the after\nthe normal parts\n\nthe grocery lists were the real me'
                  },

                  'untitled_45.txt': {
                    type: 'file',
                    name: 'untitled_45.txt',
                    icon: 'file-txt',
                    modified: '2023-11-17T02:33:00',
                    size: 44,
                    content: 'make the bread pudding, diane\nevery thanksgiving\ndon\'t stop'
                  },

                  'untitled_46.txt': {
                    type: 'file',
                    name: 'untitled_46.txt',
                    icon: 'file-txt',
                    modified: '2023-11-17T02:41:00',
                    size: 67,
                    content: 'i don\'t want this to be a suicide note\nit isn\'t\ni just ran out of time'
                  },

                  'untitled_47.txt': {
                    type: 'file',
                    name: 'untitled_47.txt',
                    icon: 'file-txt',
                    modified: '2023-11-17T03:43:00',
                    size: 38,
                    content: '3:47\n\nokay'
                  }
                }
              }
            }
          }
        }
      }
    }
  },

  'Applications': {
    type: 'folder',
    name: 'Applications',
    children: {
      'Mail.app':       { type: 'app', name: 'Mail.app' },
      'Safari.app':     { type: 'app', name: 'Safari.app' },
      'TextEdit.app':   { type: 'app', name: 'TextEdit.app' },
      'Terminal.app':   { type: 'app', name: 'Terminal.app' },
      'Photos.app':     { type: 'app', name: 'Photos.app' },
      'Calendar.app':   { type: 'app', name: 'Calendar.app' }
    }
  },

  'Library': {
    type: 'folder',
    name: 'Library',
    children: {
      'Logs': {
        type: 'folder',
        name: 'Logs',
        children: {
          'system.log': {
            type: 'file',
            name: 'system.log',
            icon: 'file-log',
            modified: '2023-11-18T03:47:00',
            size: 245000,
            content: [
              'Nov 17 23:59:01 elena-marsh-macbook com.apple.securityd[89]: Session 0x7f9a3c01e000 created',
              'Nov 18 00:00:03 elena-marsh-macbook syslogd[60]: Configuration loaded',
              'Nov 18 00:02:17 elena-marsh-macbook com.apple.launchd[1]: (com.apple.apsd) Exited normally',
              'Nov 18 00:05:44 elena-marsh-macbook WindowServer[182]: Session 257 on console',
              'Nov 18 00:12:03 elena-marsh-macbook spotlightindexer[442]: Indexing paused (low power)',
              'Nov 18 00:15:22 elena-marsh-macbook com.apple.Dock.extra[1027]: Memory warning (threshold: 90%)',
              'Nov 18 00:31:07 elena-marsh-macbook loginwindow[95]: Screen saver started',
              'Nov 18 01:02:44 elena-marsh-macbook com.apple.securityd[89]: Keychain unlocked',
              'Nov 18 01:02:44 elena-marsh-macbook loginwindow[95]: Screen saver stopped',
              'Nov 18 01:02:45 elena-marsh-macbook Dock[1023]: Application launched: com.apple.finder',
              'Nov 18 01:03:12 elena-marsh-macbook Dock[1023]: Application launched: com.apple.Safari',
              'Nov 18 01:15:00 elena-marsh-macbook Safari[1204]: Navigation: https://www.webmd.com/cancer/...',
              'Nov 18 01:17:33 elena-marsh-macbook Safari[1204]: Navigation: https://www.mayoclinic.org/tests-procedures/...',
              'Nov 18 01:24:51 elena-marsh-macbook Safari[1204]: Navigation: https://www.cancer.org/treatment/...',
              'Nov 18 01:31:08 elena-marsh-macbook Safari[1204]: Navigation: https://www.reddit.com/r/cancer/...',
              'Nov 18 01:44:22 elena-marsh-macbook Safari[1204]: Navigation: https://www.hospicefoundation.org/...',
              'Nov 18 01:58:00 elena-marsh-macbook Safari[1204]: Navigation: https://mail.google.com/mail/u/0/...',
              'Nov 18 02:01:17 elena-marsh-macbook Safari[1204]: Navigation: https://www.etsy.com/search?q=custom+memory+box',
              'Nov 18 02:15:44 elena-marsh-macbook Dock[1023]: Application launched: com.apple.TextEdit',
              'Nov 18 02:16:01 elena-marsh-macbook TextEdit[1402]: Document opened: /Users/elena.marsh/Desktop/dont_open/untitled_45.txt',
              'Nov 18 02:23:33 elena-marsh-macbook TextEdit[1402]: Document saved: /Users/elena.marsh/Desktop/dont_open/untitled_45.txt',
              'Nov 18 02:33:11 elena-marsh-macbook TextEdit[1402]: Document opened: /Users/elena.marsh/Desktop/dont_open/untitled_46.txt',
              'Nov 18 02:41:09 elena-marsh-macbook TextEdit[1402]: Document saved: /Users/elena.marsh/Desktop/dont_open/untitled_46.txt',
              'Nov 18 02:55:00 elena-marsh-macbook Safari[1204]: Navigation: https://www.amazon.com/s?k=photo+album+leather',
              'Nov 18 03:02:17 elena-marsh-macbook Safari[1204]: Navigation: https://www.google.com/search?q=how+to+leave+things+for+people+after',
              'Nov 18 03:12:44 elena-marsh-macbook Safari[1204]: Navigation: https://www.google.com/search?q=does+anyone+know+you+were+here',
              'Nov 18 03:22:00 elena-marsh-macbook TextEdit[1402]: Document opened: /Users/elena.marsh/Desktop/dont_open/untitled_47.txt',
              'Nov 18 03:33:17 elena-marsh-macbook com.apple.securityd[89]: Keychain locked',
              'Nov 18 03:33:17 elena-marsh-macbook Safari[1204]: Session ended',
              'Nov 18 03:43:09 elena-marsh-macbook TextEdit[1402]: Document saved: /Users/elena.marsh/Desktop/dont_open/untitled_47.txt',
              'Nov 18 03:43:11 elena-marsh-macbook TextEdit[1402]: Application terminated',
              'Nov 18 03:44:00 elena-marsh-macbook Finder[1102]: Last window closed',
              'Nov 18 03:47:00 elena-marsh-macbook kernel[0]: hfs: mounted Macintosh HD on /',
              'Nov 18 03:47:00 elena-marsh-macbook kernel[0]: *** SYSTEM CLOCK HALTED ***',
              'Nov 18 03:47:00 --- END OF LOG ---'
            ].join('\n')
          }
        }
      }
    }
  }
}
},

/* ─── Browser History ─── The search queries of someone running out of time */

browserHistory: [
  { date: '2023-11-17T15:22:00', url: 'https://www.google.com/search?q=roast+chicken+cooking+time', title: 'roast chicken cooking time - Google Search' },
  { date: '2023-11-17T15:24:00', url: 'https://www.allrecipes.com/recipe/229293/classic-roast-chicken/', title: 'Classic Roast Chicken - Allrecipes' },
  { date: '2023-11-17T16:45:00', url: 'https://www.google.com/search?q=nearest+24+hour+pharmacy', title: 'nearest 24 hour pharmacy - Google Search' },
  { date: '2023-11-17T17:12:00', url: 'https://www.cvs.com/store-locator/', title: 'CVS Pharmacy - Store Locator' },
  { date: '2023-11-17T19:33:00', url: 'https://www.youtube.com/watch?v=rMq7i4yLPqk', title: 'YouTube - Cat Videos Compilation 2023' },
  { date: '2023-11-17T20:15:00', url: 'https://www.netflix.com/browse', title: 'Netflix - Home' },
  { date: '2023-11-17T21:02:00', url: 'https://mail.google.com/mail/u/0/#inbox', title: 'Gmail - Inbox (3)' },
  { date: '2023-11-17T21:30:00', url: 'https://www.google.com/search?q=how+to+tell+your+family+you+are+dying', title: 'how to tell your family you are dying - Google Search' },
  { date: '2023-11-17T21:30:45', url: 'https://www.google.com/search?q=how+to+tell+your+sister+you+are+sick', title: 'how to tell your sister you are sick - Google Search' },
  { date: '2023-11-17T21:34:00', url: 'https://www.google.com/search?q=terminal+illness+how+to+tell+family', title: 'terminal illness how to tell family - Google Search' },
  { date: '2023-11-17T21:45:00', url: 'https://www.reddit.com/r/TrueOffMyChest/comments/17nqp3t/', title: "r/TrueOffMyChest - I found out I'm dying and I can't tell my family" },
  { date: '2023-11-17T22:12:00', url: 'https://www.google.com/search?q=letter+to+family+when+you+are+dying', title: 'letter to family when you are dying - Google Search' },
  { date: '2023-11-17T22:15:00', url: 'https://www.hospicefoundation.org/Communicating-About-Illness', title: 'How to Communicate About Serious Illness \u2014 Hospice Foundation' },
  { date: '2023-11-17T22:30:00', url: 'https://www.google.com/search?q=refractory+cancer+life+expectancy+32+female', title: 'refractory cancer life expectancy 32 female - Google Search' },
  { date: '2023-11-17T22:30:12', url: 'https://www.google.com/search?q=aml+refractory+prognosis+young+adult', title: 'aml refractory prognosis young adult - Google Search' },
  { date: '2023-11-17T22:31:00', url: 'https://www.cancer.org/cancer/acute-myeloid-leukemia/treating/recurrence.html', title: "Treating Acute Myeloid Leukemia (AML) That Doesn't Respond or Comes Back" },
  { date: '2023-11-17T22:45:00', url: 'https://www.google.com/search?q=when+someone+dies+what+happens+to+their+cat', title: 'when someone dies what happens to their cat - Google Search' },
  { date: '2023-11-17T23:00:00', url: 'https://www.google.com/search?q=how+to+make+sure+someone+finds+your+body+quickly', title: 'how to make sure someone finds your body quickly - Google Search' },
  { date: '2023-11-17T23:15:00', url: 'https://www.google.com/search?q=dying+alone+what+happens+to+belongings', title: 'dying alone what happens to belongings - Google Search' },
  { date: '2023-11-18T01:02:44', url: 'https://www.webmd.com/cancer/aml/default.htm', title: 'Acute Myeloid Leukemia - WebMD' },
  { date: '2023-11-18T01:17:33', url: 'https://www.mayoclinic.org/tests-procedures/bone-marrow-biopsy/about/pac-20393125', title: 'Bone marrow biopsy - Mayo Clinic' },
  { date: '2023-11-18T01:24:51', url: 'https://www.cancer.org/treatment/survivorship-during-and-after-treatment/understanding-recurrence.html', title: 'Understanding Cancer Recurrence' },
  { date: '2023-11-18T01:31:08', url: 'https://www.reddit.com/r/cancer/comments/17nr2xk/', title: 'r/cancer - How do you deal with knowing?' },
  { date: '2023-11-18T01:44:22', url: 'https://www.hospicefoundation.org/When-to-Call-Hospice', title: 'When to Call Hospice \u2014 Hospice Foundation' },
  { date: '2023-11-18T01:58:00', url: 'https://mail.google.com/mail/u/0/#inbox', title: 'Gmail - Inbox (3)' },
  { date: '2023-11-18T02:01:17', url: 'https://www.etsy.com/search?q=custom+memory+box', title: 'Custom Memory Box - Etsy' },
  { date: '2023-11-18T02:15:00', url: 'https://www.google.com/search?q=will+without+lawyer+small+estate', title: 'will without lawyer small estate - Google Search' },
  { date: '2023-11-18T02:55:00', url: 'https://www.amazon.com/s?k=photo+album+leather', title: 'Amazon.com: leather photo album' },
  { date: '2023-11-18T03:02:17', url: 'https://www.google.com/search?q=how+to+leave+things+for+people+after+you+die', title: 'how to leave things for people after you die - Google Search' },
  { date: '2023-11-18T03:12:44', url: 'https://www.google.com/search?q=does+anyone+know+you+were+here', title: 'does anyone know you were here - Google Search' },
  { date: '2023-11-18T03:22:00', url: 'https://www.google.com/search?q=clock+stopped+at+347', title: 'clock stopped at 3:47 - Google Search' }
],

/* ─── Email Inbox ─── */

emailInbox: [
  {
    from: 'Diane Marsh <diane.marsh@gmail.com>',
    to: 'elena.marsh@tidaldesign.co',
    date: '2023-11-17T18:22:00',
    subject: 'Tomorrow!',
    read: true,
    starred: true,
    body: 'Hey El,\n\nJust confirming \u2014 I\'m coming over tomorrow around 5 for dinner!\n\nI\'m bringing wine. Red okay? I know you usually don\'t but it\'s cold\noutside and red wine season, sorry I don\'t make the rules.\n\nAlso I\'m bringing the good bread from that bakery on Elm. The one\nwith the rosemary.\n\nShould I bring anything else? Ice cream? Pie? I could bring pie.\n\nCAN\'T WAIT TO SEE YOUUUUU\n\n\u2014 D\n\nPS: Tell Mochi I\'m coming and she better be nice to me this time.'
  },
  {
    from: 'Diane Marsh <diane.marsh@gmail.com>',
    to: 'elena.marsh@tidaldesign.co',
    date: '2023-11-17T18:22:45',
    subject: 'Re: Tomorrow!',
    read: true,
    starred: true,
    body: 'PS again:\n\nI had a weird feeling today. Like I should call you. I don\'t know why.\n\nYou\'d tell me if something was wrong, right?\n\nOf course you would. Never mind.\n\nSee you tomorrow. Love you.'
  },
  {
    from: 'Karen Whitfield <k.whitfield@meridianhealth.org>',
    to: 'elena.marsh@tidaldesign.co',
    date: '2023-11-14T16:38:00',
    subject: 'Re: Thursday meeting \u2014 rescheduling?',
    read: true,
    starred: false,
    body: 'Elena, are you okay? You didn\'t make the meeting.\n\nI tried calling. Your phone went straight to voicemail.\n\nThe deadline is December 1st. I need to know if you can still deliver.\nIf you\'re dealing with something, just tell me. I can extend if needed.\n\nPlease just let me know you\'re alright.\n\nKaren'
  },
  {
    from: 'noreply@chase.com',
    to: 'elena.marsh@tidaldesign.co',
    date: '2023-11-15T06:00:00',
    subject: 'Your November Statement is Ready',
    read: true,
    starred: false,
    body: 'Your Chase Business Checking statement for November 2023 is ready\nto view online.\n\nAccount ending in: 7291\nStatement period: 10/16/2023 - 11/15/2023\n\nCurrent balance: $6,847.23\n\n[View Statement Online]'
  },
  {
    from: 'Dr. Sarah Chen <schen@westside-oncology.com>',
    to: 'elena.marsh@tidaldesign.co',
    date: '2023-11-13T10:15:00',
    subject: 'Re: Follow-up questions',
    read: true,
    starred: true,
    body: 'Dear Elena,\n\nThank you for your questions. I want to be straightforward with you.\n\nThe results from the bone marrow biopsy confirm what we discussed.\nThe induction therapy did not achieve complete remission. At this\nstage, the options are:\n\n1. Salvage chemotherapy (FLAG-IDA) \u2014 approximately 20-30% response rate\n2. Clinical trial enrollment \u2014 I can refer you to Dr. Morrison at\n   University Hospital\n3. Palliative care focus\n\nI know this is not what you were hoping to hear. I want to emphasize\nthat the decision is yours, and there is no wrong choice.\n\nCan we schedule an appointment this week to discuss in person?\nPlease bring anyone you\'d like to have with you.\n\nWarmly,\nDr. Sarah Chen\nWestside Oncology Associates\n\nCONFIDENTIAL: This email contains protected health information.'
  },
  {
    from: 'Marcus Webb <mwebb@gmail.com>',
    to: 'elena.marsh@tidaldesign.co',
    date: '2023-11-10T12:45:00',
    subject: 'Re: Dinner next week?',
    read: true,
    starred: false,
    body: 'Hey El,\n\nYeah let\'s do Wednesday! Ramen place on 5th?\n\nAlso \u2014 and I don\'t want to be weird about this \u2014 you seem kind of\noff lately. Everything good?\n\nIf you\'re busy with the Meridian thing I get it. Just checking.\n\n-M'
  },
  {
    from: 'noreply@apple.com',
    to: 'elena.marsh@tidaldesign.co',
    date: '2023-11-01T09:00:00',
    subject: 'Your iCloud storage is almost full',
    read: true,
    starred: false,
    body: 'Your iCloud storage is 94% full.\n\n4.7 GB of 5 GB used.\n\n[Upgrade Storage] | [Manage Storage]'
  },
  {
    from: 'Diane Marsh <diane.marsh@gmail.com>',
    to: 'elena.marsh@tidaldesign.co',
    date: '2023-10-29T19:30:00',
    subject: "Mom's birthday",
    read: true,
    starred: true,
    body: 'Hey, so Mom\'s 60th is December 8th. I know it\'s a ways off but\nI want to plan something.\n\nIdeas:\n- Surprise party at that Italian place she loves\n- Weekend trip somewhere (she always talks about wanting to see Savannah)\n- Just us three + dinner + something sentimental\n\nI\'m leaning toward the last one. She\'s not a big party person.\n\nWhat do you think? You\'re better at the gift stuff than me.\n\nD'
  },
  {
    from: 'Dr. Sarah Chen <schen@westside-oncology.com>',
    to: 'elena.marsh@tidaldesign.co',
    date: '2023-09-22T16:45:00',
    subject: 'Re: Pathology results',
    read: true,
    starred: true,
    body: 'Dear Elena,\n\nThe pathology report is back. I\'d like to discuss the results with\nyou in person.\n\nCould you come to the office this Friday at 2 PM? I\'ve reserved\nextra time so we can go through everything thoroughly.\n\nPlease don\'t hesitate to reach out if you need anything before then.\n\nDr. Sarah Chen\nWestside Oncology Associates'
  }
],

/* ─── Calendar ─── Plans she made for a future she wouldn't see */

calendarEvents: [
  { date: '2023-11-18T17:00:00', title: 'Diane \u2014 dinner', color: 'red', notes: 'roast chicken, bread pudding (try the recipe), candles, wine (she\'s bringing red)' },
  { date: '2023-11-20T19:00:00', title: 'Marcus \u2014 ramen', color: 'blue', notes: '5th street. tonkotsu. don\'t let him pay again.' },
  { date: '2023-11-22',         title: 'Thanksgiving',    color: 'orange', notes: "at Mom's. bring the bread pudding. call Diane about rides." },
  { date: '2023-12-01',         title: 'Meridian deadline', color: 'purple', notes: "finish it. or hand it off. or don't." },
  { date: '2023-12-05T14:00:00', title: 'Dentist \u2014 Dr. Patel', color: 'green', notes: '6-month cleaning. insurance card in the drawer.' },
  { date: '2023-12-08',         title: "Mom's 60th",      color: 'red', notes: "she wants something sentimental. what do you give someone you're leaving?" },
  { date: '2023-12-25',         title: 'Christmas',        color: 'red', notes: '' },
  { date: '2023-12-31',         title: "New Year's Eve",  color: 'yellow', notes: '\u2014' }
],

/* ─── Stickies ─── */

stickies: [
  { color: 'yellow', text: 'call Dr. Chen back', modified: '2023-11-13T14:22:00' },
  { color: 'yellow', text: 'Mochi vet appointment \u2014 shots due?', modified: '2023-11-10T09:00:00' },
  { color: 'pink',   text: 'the Meridian blue is #4A7C9B\nKaren will know it when she sees it', modified: '2023-11-12T23:45:00' },
  { color: 'yellow', text: 'grocery run before Saturday\nDiane is coming at 5', modified: '2023-11-17T08:30:00' },
  { color: 'blue',   text: 'finish the letters', modified: '2023-11-17T03:00:00' }
],

wallpaper: 'macos-catalina'
};

/*
 * November 2023 starts on Wednesday.
 * November 18 is a Saturday.
 * The clock reads: Sat Nov 18  3:47 AM
 */
