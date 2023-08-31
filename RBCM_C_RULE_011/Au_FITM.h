/******************************************************************************
*****     (C) COPYRIGHT Robert Bosch GmbH - All Rights Reserved           *****
******************************************************************************/
/*!
 * \file         Au_FITM.h
 * \brief        Fault injection test manager routes the test request from App.SafeTestManager
 *               to appropriate Safety Mechanism fault injection function
 *
 * \copyright (C) 2020 Robert Bosch GmbH.
 *          The reproduction, distribution and utilization of this file as
 *          well as the communication of its contents to others without express
 *          authorization is prohibited. Offenders will be held liable for the
 *          payment of damages. All rights reserved in the event of the grant
 *          of a patent, utility model or design.
 */

/* QAC - Overview: All Warnings that occure in that Files                    */

/* QAC1: UNUSED IDENTIFIER                                               [3] */
/* PRQA S 3205 - Identifier is never used and could be removed               */
/* Identifier may be used later. Warning can be ignored.                     */

#ifndef AU_FITM_H
#define AU_FITM_H

/*=============================================================================
=======                       INCLUDES                                  =======
=============================================================================*/

/*------ standard includes -------*/

/*------ project includes --------*/
#include "FIT_PFlash_if.h"
#include "FIT_MPU_if.h"
#include "FIT_Wdg_if.h"
#include "FIT_RAMMonitoring_if.h"


/*------ module includes --------*/
#include "Au_FITM_Cfg.h"
#include "Au_FITM_if.h"
#include "FIT_ClockMon_if.h"

#ifdef STARTUP_APP_ACTIVE
#include "FIT_REGM_if.h"
#endif

/*=============================================================================
=======                       DEFINES                                   =======
=============================================================================*/


#define SAFETESTDRV_PFLASH_MAXTC_CNT_ASIL     24u
#define SAFETESTDRV_PFLASH_MAXTC_CNT_QM       24u
#define SAFETESTDRV_PFLASH_MAXTC_CNT_QM       24u
#define SAFETESTDRV_TRAP_MAXTC_CNT_ASIL       ((uint8)SAFETESTDRV_MPU_TRAP_MAX_TC_PER_CORE*(uint8)2)
#define SAFETESTDRV_TRAP_MAXTC_CNT_QM         ((uint8)SAFETESTDRV_MPU_TRAP_MAX_TC_PER_CORE*(uint8)2)
#define SAFETESTDRV_WDGM_ASIL_MAXTC_CNT       (uint8)FIT_WDGM_MAXIMUM_ASIL_TEST_CASES
#define SAFETESTDRV_WDGM_QM_MAXTC_CNT         (uint8)FIT_WDGM_MAXIMUM_QM_TEST_CASES
#define SAFETESTDRV_PERIPROT_MAXTC_CNT_ASIL   ((uint8)SAFETESTDRV_PERIPROT_MAX_TC_PER_CORE*(uint8)2)
#define SAFETESTDRV_PERIPROT_MAXTC_CNT_QM     ((uint8)SAFETESTDRV_PERIPROT_MAX_TC_PER_CORE*(uint8)2)
#define SAFETESTDRV_MPU_MP_MAXTC_CNT_ASIL     (uint8)SAFETESTDRV_MPU_MP_ASIL_MAXTC_CNT
#define SAFETESTDRV_MPU_MP_MAXTC_CNT_QM       (uint8)SAFETESTDRV_MPU_MP_QM_MAXTC_CNT

#define AU_FITM_CORE0 0U
#define AU_FITM_CORE1 1U

/*==============================================================================
==============   TYPE DEFINES                                        ===========
===============================================================================*/
typedef struct {
uint8* Au_FITM_DataPtr;
uint8 Au_FITM_DataValue;
}Au_FITM_data_t; /* PRQA S 3205 *//*  QAC1*/

/*===============================================================================
==============           VARIABLES                                ===============
===============================================================================*/

extern const uint8 Safety_Apps_No_Of_Testcases[SAFETESTDRV_MAX_NUMBER_OF_SM];

/*===============================================================================
==============           FUNCTIONS                                ===============
===============================================================================*/

/*------------------------------------------------------------------------------
 *  FUNCTION:   Au_FITM_MainFunction_ASIL(void)
 */
/*! \brief      This is the ASIL runnable mapped to 100ms task and it switches to different
 *              functions depending on the core ID.
 * \param       void
 * \return      void
 * \pre         None
 * \post        None
 * \warning     None
 * \attention   None
 * \todo        None
 *
 *
*//*--------------------------------------------------------------------------*/
void Au_FITM_MainFunction_ASIL(void);

/*------------------------------------------------------------------------------
 *  FUNCTION:   Au_FITM_MainFunction_QM(void)
 */
/*! \brief      This is the QM runnable mapped to 100ms task and it switches to
 *              different functions depending on the core ID.
 * \param       void
 * \return      void
 * \pre         None
 * \post        None
 * \warning     None
 * \attention   None
 * \todo        None
 *
 *
*//*--------------------------------------------------------------------------*/
void Au_FITM_MainFunction_QM(void);

#endif
