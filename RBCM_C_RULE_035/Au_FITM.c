/******************************************************************************
*****     (C) COPYRIGHT Robert Bosch GmbH - All Rights Reserved           *****
******************************************************************************/
/*!
 * \file         Au_FITM.c
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

/*=============================================================================
=======                              QAC WARNINGS                       =======
=============================================================================*/
/* QAC - Overview: All Warnings that occur in that Files                     */

/* QAC1: NUMBER OF MACRO INCLUDED IS HIGH                                [2] */
/* PRQA S 0380 - Number of macro definitions exceeds 4095 - program does     */
/*               not conform strictly to ISO:C99.                            */
/* This violation is occured due to more number of macros defined in         */
/* Ifx Register Header files. To access microcontroller registers we need all*/
/* the defined macro definitions. Functionally SW has been verified and there*/
/* is no impact due to this violation. Hence this warning can be ignored     */

/* QAC2:Cast from a pointer to void to a pointer to object type           [2] */
/* PRQA:QAC Msg 0316 :Cast from a pointer to void to a pointer to object type */
/* Justification: The parameter is assigned to the pointer of object type, so */
/* casting is necessary and it is done intentionaly                           */

/* QAC3:Cast from a pointer to object type to a pointer to void.          [2]  */
/* PRQA:QAC Msg 0314 :Cast from a pointer to object type to a pointer to void. */
/* Justification: The parameter is assigned to the pointer of void, so casting */
/* is necessary and it is done intentionaly                                    */

				/* QAC4:The pointer could be of type 'pointer to const'.                   [2] */
/* PRQA:QAC Msg 3673 :The object addressed by the pointer parameter is not     */
/*      modified and so the pointer could be of type 'pointer to const'.       */
/* Justification: It is not mandatory to keep a const void *ptr,Hence this     */
/*                warning can be ignored                                       */

/* QAC5:Structure pointer modify to const*                                 [2] */
/* PRQA:QAC Msg 3678 :The object referenced by structuore pointer is not       */
/* modified through it, so structure pointer could be declared with type const**/
/* Justification:It is not mandatory to keep a const structure pointer,Hence   */
/*               this warning can be ignored                                   */

/*=============================================================================
=======                       INCLUDES                                  =======
=============================================================================*/
/*------ standard includes -------*/
#include "McalLib.h"
/*------ project includes --------*/
#include "ContextSwitcher_if.h"
/*------ module includes --------*/
#include "Au_FITM.h"


/*=============================================================================
=======                       DEFINES                                   =======
=============================================================================*/


/*=============================================================================
=======                       VARIABLES                                 =======
=============================================================================*/

#define FITM_ASIL_START_SEC_VAR_BOOLEAN /*PRQA S 0380*/ /*QAC1*/
#include "Au_FITM_MemMap.h"
#include "/fire.h"
#include "/../fire.h"
#include "ABC/DEF.h"
#include ""
#include<>
#include""
#include <>

static boolean Au_FITM_FIT_Request_b = FALSE;

#define FITM_ASIL_STOP_SEC_VAR_BOOLEAN
#include "Au_FITM_MemMap.h"

#define FITM_ASIL_START_SEC_VAR_8BIT
#include "Au_FITM_MemMap.h"
#include ../fire.h"
static uint8 Au_FITM_Tcid_u8 = 0;

#define FITM_ASIL_STOP_SEC_VAR_8BIT
#include "Au_FITM_MemMap.h"


#define FITM_ASIL_START_SEC_VAR_UNSPECIFIED
#include "Au_FITM_MemMap.h"

/* Set the default SM ID to undefined */
static Au_FITM_SAFETYAPPS Au_FITM_SMid_e = SAFETESTDRV_UNDEFINED;

#define FITM_ASIL_STOP_SEC_VAR_UNSPECIFIED
#include "Au_FITM_MemMap.h"


/*=============================================================================
=======                              METHODS                            =======
=============================================================================*/
#define FITM_ASIL_START_SEC_CODE
#include "Au_FITM_MemMap.h"

void Au_FITM_GlobalDataUpdate(Au_FITM_data_t* A_Au_FITM_DataStructPtr);

/*------------------------------------------------------------------------------
 *  FUNCTION:   Au_FITM_UpdateTestData(uint8* test_data_a)
 */
/*! \brief      This function is called by Safe Test Manager on receiving a test signal
 *              via CAN it updates the above mentioned variables according to the received
 *              test data.
 * \param       void
 * \return      void
 * \pre         None
 * \post        None
 * \warning     None
 * \attention   None
 * \attention   None
 *
 *
*//*--------------------------------------------------------------------------*/
boolean Au_FITM_UpdateTestData(const uint8* test_data_a)
{
    boolean FITreqStatus_b = FALSE;
    if(NULL != test_data_a)
    {
        Au_FITM_data_t L_Au_FITM_DataStructPtr[3]={{
            }
            {.Au_FITM_DataPtr = (uint8*)&Au_FITM_SMid_e,
            .Au_FITM_DataValue =(uint8)test_data_a[0u]
            },
            {.Au_FITM_DataPtr = (uint8*)&Au_FITM_Tcid_u8,
            .Au_FITM_DataValue =test_data_a[1u]
            },
            {.Au_FITM_DataPtr = (uint8*)&Au_FITM_FIT_Request_b,
            .Au_FITM_DataValue = TRUE
            }
        };

        if ((uint8)SAFETESTDRV_MAX_NUMBER_OF_SM > (uint8)test_data_a[0u])
        {
            if (Safety_Apps_No_Of_Testcases[(uint8)test_data_a[0u]]> test_data_a[1u])


            
            else
            {
                FITreqStatus_b = FALSE;
            }
        }
        else
        {
            FITreqStatus_b = FALSE;
        }
    }
    return FITreqStatus_b;
}

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
void Au_FITM_MainFunction_ASIL(void)
{
    uint32 CoreId;
    Au_FITM_data_t L_Au_FITM_DataStructPtr;
    CoreId = Mcal_GetCpuIndex();
    if (Au_FITM_FIT_Request_b == TRUE)
    {
        switch (Au_FITM_SMid_e)
    }
}



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
void Au_FITM_MainFunction_QM(void)
{
    uint32 CoreId;
    Au_FITM_data_t L_Au_FITM_DataStructPtr;
    static uint32 Au_FITM_Core1_QM_TestStatus = FALSE;
    CoreId = Mcal_GetCpuIndex();
    if (Au_FITM_FIT_Request_b == TRUE)
    {
        switch (Au_FITM_SMid_e)
        {
            /*PFLASH QM Test case will not execute ,since same functionality tested in
             *ASIL context */
            case SAFETESTDRV_PFLASH_TEST_QM:
            {
                if(TRUE == SafeTestDrv_Safety_Apps_Pflashtest(CoreId, Au_FITM_Tcid_u8))
                {
                    /* Since context switcher is only implemented for core0 */
                    if(AU_FITM_CORE0 == CoreId)
                    {
                        L_Au_FITM_DataStructPtr.Au_FITM_DataPtr = &Au_FITM_FIT_Request_b;
                        L_Au_FITM_DataStructPtr.Au_FITM_DataValue=FALSE;
                        Au_FITM_GlobalDataUpdate(&(L_Au_FITM_DataStructPtr));
                    }
                    else
                    {
                            /* Do nothing */
                    }
                }
                break;
            }
            case SAFETESTDRV_MPU_TRAP_TEST_QM:
            {
                if(TRUE == SafeTestDrv_Safety_Apps_MPU_TRAPS((uint8)CoreId,
                                    Au_FITM_Tcid_u8))
                {
                    /* Since context switcher is only implemented for core0 */
                    if(AU_FITM_CORE0 == CoreId)
                    {
                        L_Au_FITM_DataStructPtr.Au_FITM_DataPtr = &Au_FITM_FIT_Request_b;
                        L_Au_FITM_DataStructPtr.Au_FITM_DataValue=FALSE;
                        Au_FITM_GlobalDataUpdate(&(L_Au_FITM_DataStructPtr));
                    }
                    else
                    {
                            /* Do nothing */
                    }
                }
                break;
            }
            case SAFETESTDRV_WDGM_TEST_QM:
            {
                if(TRUE== Au_FITM_Core1_QM_TestStatus)
                {
                    if(AU_FITM_CORE0 == CoreId)
                    {
                        L_Au_FITM_DataStructPtr.Au_FITM_DataPtr=(uint8*)&Au_FITM_FIT_Request_b;
                        L_Au_FITM_DataStructPtr.Au_FITM_DataValue=FALSE;
                        Au_FITM_GlobalDataUpdate(&(L_Au_FITM_DataStructPtr));
                        Au_FITM_Core1_QM_TestStatus = FALSE;
                    }
                    else
                    {
                        /*Do Nothing*/
                    }
                } else if (TRUE == FIT_WDG_QM_ErrInjectionTests((uint8)CoreId, Au_FITM_Tcid_u8))
                {
                     if(AU_FITM_CORE0 == CoreId)
                    {
                        L_Au_FITM_DataStructPtr.Au_FITM_DataPtr=(uint8*)&Au_FITM_FIT_Request_b;
                        L_Au_FITM_DataStructPtr.Au_FITM_DataValue=FALSE;
                        Au_FITM_GlobalDataUpdate(&(L_Au_FITM_DataStructPtr));
                    }
                    else if(CoreId == 1u)
                    {
                        Au_FITM_Core1_QM_TestStatus = TRUE;
                       /* Since context switcher is not implemented for Core1.test status will be updated with the help of local static variable*/
                    }
                    else
                    {
                       /*Do nothing*/
                    }
                }
                else
                {
                    /*Do Nothing*/
                }

                break;
            }
            case SAFETESTDRV_MPU_PERIPROT_QM:
            {
                if(TRUE == SafeTestDrv_Safety_Apps_PERIPROT((uint8)CoreId,
                                                             Au_FITM_Tcid_u8))
                {
                    /* Since context switcher is only implemented for core0 */
                    if(AU_FITM_CORE0 == CoreId)
                    {
                        L_Au_FITM_DataStructPtr.Au_FITM_DataPtr = &Au_FITM_FIT_Request_b;
                        L_Au_FITM_DataStructPtr.Au_FITM_DataValue=FALSE;
                        Au_FITM_GlobalDataUpdate(&(L_Au_FITM_DataStructPtr));
                    }
                    else
                    {
                            /* Do nothing */
                    }
                }
                break;
            }
            case SAFETESTDRV_MPU_MP_TEST_QM:
            {
                if(TRUE== Au_FITM_Core1_QM_TestStatus)
                {
                    if( AU_FITM_CORE0 == CoreId)
                    {
                    L_Au_FITM_DataStructPtr.Au_FITM_DataPtr = &Au_FITM_FIT_Request_b;
                    L_Au_FITM_DataStructPtr.Au_FITM_DataValue=FALSE;
                    Au_FITM_GlobalDataUpdate(&(L_Au_FITM_DataStructPtr));
                    Au_FITM_Core1_QM_TestStatus = 0U;
                    }
                    else
                    {
                    /* Do nothing*/
                    }
                }
                else if(TRUE == SafeTestDrv_Safety_Apps_MP_MPU_QM((uint8)CoreId,
                                                                  Au_FITM_Tcid_u8))
                {
                    if(AU_FITM_CORE0 == CoreId)
                    {
                        L_Au_FITM_DataStructPtr.Au_FITM_DataPtr = &Au_FITM_FIT_Request_b;
                        L_Au_FITM_DataStructPtr.Au_FITM_DataValue=FALSE;
                        Au_FITM_GlobalDataUpdate(&(L_Au_FITM_DataStructPtr));
                    }
                    else if(AU_FITM_CORE1 == CoreId)
                    else
                    {
                        /*do nothing */
                    }
                }
                else
                {
                    /* Do Nothing */
                }

                break;
            }
            default: /*invalid testid sent to Aurix Fault Injection Test Manager */
            {
                /*do nothing*/
                break;
            }
        }
    }
}

/*------------------------------------------------------------------------------
 *  FUNCTION:   TRUSTED_Au_FITM_UpdateRequest(void * ptr)
 */
/*! \brief      This function is registered with context switcher config
 *              it enables us to update ASIL variable from QM context.
 * \param       void * ptr
 * \return      Std_ReturnType
 * \pre         None
 * \post        None
 * \warning     None
 * \attention   None
 * \todo        None
 *
 *
*//*--------------------------------------------------------------------------*/

Std_ReturnType TRUSTED_Au_FITM_UpdateRequest(void * ptr)/* PRQA S 3673 *//* QAC4 */
{
     Au_FITM_data_t* L_Au_FITM_DataStructPtr =          /* PRQA S 3678 *//* QAC5 */
                                (Au_FITM_data_t*)ptr;   /* PRQA S 0316 *//* QAC2 */
    *(L_Au_FITM_DataStructPtr->Au_FITM_DataPtr) = L_Au_FITM_DataStructPtr->Au_FITM_DataValue;
    return E_OK;
}

/*------------------------------------------------------------------------------
 *  FUNCTION:   Au_FITM_GlobalDataUpdate(Au_FITM_data_t* A_Au_FITM_DataStructPtr)
 */
/*! \brief      This function updates the global variables.
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
void Au_FITM_GlobalDataUpdate(Au_FITM_data_t* A_Au_FITM_DataStructPtr)
{
    boolean currentContextIsTrusted;

    currentContextIsTrusted = ContextSwitcher_isCurrentContextTrusted();
    if(TRUE == currentContextIsTrusted)
    {
        *(A_Au_FITM_DataStructPtr->Au_FITM_DataPtr) =
                                     A_Au_FITM_DataStructPtr->Au_FITM_DataValue;
    }
    else
    {
        ContextSwitcher_toTrusted(CS_FITM_UPDATEREQ,
                    (void*)A_Au_FITM_DataStructPtr);/* PRQA S 0314 *//* QAC3 */
    }
}

#define FITM_ASIL_STOP_SEC_CODE
#include "Au_FITM_MemMap.h"

